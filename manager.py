
import argparse
import os
import shutil

def create_admin(username, password):
    admin_file_path = os.path.join('APelahishokr', 'admin.txt')
    if os.path.exists(admin_file_path):
        print("Error: Admin already exists.")
        return

    os.makedirs(os.path.dirname(admin_file_path), exist_ok=True)
    with open(admin_file_path, 'w') as file:
        file.write(f'Username: {username}\nPassword: {password}')
    print("Admin created successfully.")
def purge_data():
    accounts_file = os.path.join('APelahishokr', 'accounts.csv')
    projects_file = os.path.join('APelahishokr', 'projects.json')
    
    if not os.path.exists(accounts_file) and not os.path.exists(projects_file):
        print("Error: Data files do not exist.")
        return

    confirm = input("Are you sure you want to purge all data? This action cannot be undone. Type 'YES' to confirm: ")
    if confirm == 'YES':
        if os.path.exists(accounts_file):
            os.remove(accounts_file)
        if os.path.exists(projects_file):
            os.remove(projects_file)
        print("All data has been purged.")
    else:
        print("Data purge canceled.")

