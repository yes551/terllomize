
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
