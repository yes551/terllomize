import pandas as pd
import hashlib
from rich.console import Console
from rich.table import Table
from loguru import logger

console = Console()

def load_admin_credentials(admin_file='.\\APelahishokr\\admin.txt'):
    with open(admin_file, 'r') as file:
        lines = file.read().splitlines()
    if len(lines) < 2 or not lines[0].startswith('Username:') or not lines[1].startswith('Password:'):
        raise ValueError("Admin file must contain a username and a password in the format 'username:' and 'password:'.")
    admin_username = lines[0].split('Username:')[1].strip()
    admin_password = lines[1].split('Password:')[1].strip()
    return admin_username, admin_password
class UserAccount:
    def __init__(self, accounts_file):
        self.accounts_file = accounts_file
        self.accounts = self.load_accounts()
        logger.add(".\\APelahishokr\\application.log", rotation="1 MB")

    def load_accounts(self):
        logger.info("Loading accounts from {}", self.accounts_file)
        try:
            return pd.read_csv(self.accounts_file)
        except FileNotFoundError:
            logger.warning("Accounts file not found, creating a new one.")
            return pd.DataFrame(columns=['Username', 'Password', 'Email', 'Role'])

    def save_accounts(self):
        logger.info("Saving accounts to {}", self.accounts_file)
        self.accounts.to_csv(self.accounts_file, index=False)

    def encrypt_password(self, password):
        logger.info("Encrypting password")
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_up(self, username, password, email, role='user'):
        logger.info("Attempting to sign up user: {}", username)
        admin_user, _ = load_admin_credentials()
        if username in self.accounts['Username'].values or email in self.accounts['Email'].values or username == admin_user:
            console.print("[bold red]Error:[/bold red] Username or email already exists.")
            logger.warning("Sign up failed: Username or email already exists")
            return False

        encrypted_password = self.encrypt_password(password)
        new_account = pd.DataFrame({
            'Username': [username],
            'Password': [encrypted_password],
            'Email': [email],
            'Role': [role]
        })
 self.accounts = pd.concat([self.accounts, new_account], ignore_index=True)
        self.save_accounts()
        logger.info("User signed up successfully: {}", username)
        return True

    def login(self, username, password):
        admin_user, admin_pass = load_admin_credentials()
        if (username == admin_user and password == admin_pass):
            return pd.DataFrame({"Username": [admin_user], "Password": [admin_pass], "Email": [""], "Role": ["admin"]}).iloc[0]

        logger.info("Attempting to login user: {}", username)
        encrypted_password = self.encrypt_password(password)
        account = self.accounts[(self.accounts['Username'] == username) & (self.accounts['Password'] == encrypted_password)]
        if len(account) == 0:
            console.print("[bold red]Error:[/bold red] Invalid username or password.")
            logger.warning("Login failed: Invalid username or password")
            return None
        elif account["Role"].values[0] == "Inactive":
            console.print("[bold red]Error:[/bold red] Your account has been deactivated.")
            logger.warning("Login failed: deactivated account login attempt")
            return None
        else:
            console.print("[bold green]Login successful![/bold green]")
            logger.info("User logged in successfully: {}", username)
            return account.iloc[0]
def is_admin(self, account):
        return account['Role'] == 'admin'

    def modify_user_status(self):
        while True:
            # Display all accounts
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Index", style="dim", width=6)
            table.add_column("Username")
            table.add_column("Email")
            table.add_column("Role")

            for idx, row in self.accounts.iterrows():
                table.add_row(str(idx), row['Username'], row['Email'], row['Role'])

            console.print(table)
# Prompt for user selection
            index = console.input("\nEnter the index of the user to modify (or press Enter to exit): ")

            if index == "":
                break

            if not index.isdigit() or int(index) not in range(len(self.accounts)):
                console.print("[bold red]Error:[/bold red] Invalid index.")
                continue

            index = int(index)
            user_role = self.accounts.at[index, 'Role']
            new_role = 'Inactive' if user_role != 'Inactive' else 'user'
            self.accounts.at[index, 'Role'] = new_role
            self.save_accounts()

            console.print(f"[bold green]User at index {index} has been changed to {new_role}.[/bold green]")
            logger.info("User role modified: {} -> {}", self.accounts.at[index, 'Username'], new_role)
