import unittest
import os
import pandas as pd
import json
from unittest.mock import patch, mock_open
from io import StringIO
from account import UserAccount
from main import (
    load_projects,
    save_projects,
    create_project,
    add_user_to_project,
    remove_user_from_project,
    add_task,
    view_tasks_for_project,
    remove_task_from_project,
    remove_project,
    view_projects,
    can_access_project,
    manage_tasks,
    update_task_status_or_comment
)

class TestUserAccount(unittest.TestCase):

    def setUp(self):
        # Create a temporary accounts file and admin credentials
        self.accounts_file = 'test_accounts.csv'
        self.admin_file = 'test_admin.txt'
        self.projects_file = 'test_projects.json'

        with open(self.admin_file, 'w') as file:
            file.write("Username:admin\nPassword:adminpass")

        # Mocking the logger to avoid file creation
        patch('account.logger').start()

        # Initialize the UserAccount class
        self.user_account = UserAccount(self.accounts_file)

    def tearDown(self):
        # Remove the temporary files after tests
        if os.path.exists(self.accounts_file):
            os.remove(self.accounts_file)
        if os.path.exists(self.admin_file):
            os.remove(self.admin_file)
        if os.path.exists(self.projects_file):
            os.remove(self.projects_file)
        patch.stopall()

    def test_01_sign_up(self):
        print("Running test 01: test_sign_up")
        self.assertTrue(self.user_account.sign_up('testuser', 'password123', 'testuser@example.com'))
        accounts = pd.read_csv(self.accounts_file)
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts.iloc[0]['Username'], 'testuser')

    def test_02_login(self):
        print("Running test 02: test_login")
        self.user_account.sign_up('testuser', 'password123', 'testuser@example.com')
        account = self.user_account.login('testuser', 'password123')
        self.assertIsNotNone(account)
        self.assertEqual(account['Username'], 'testuser')
def test_03_login_fail(self):
        print("Running test 03: test_login_fail")
        self.user_account.sign_up('testuser', 'password123', 'testuser@example.com')
        account = self.user_account.login('testuser', 'wrongpassword')
        self.assertIsNone(account)

    def test_04_duplicate_sign_up(self):
        print("Running test 04: test_duplicate_sign_up")
        self.user_account.sign_up('testuser', 'password123', 'testuser@example.com')
        result = self.user_account.sign_up('testuser', 'password123', 'testuser@example.com')
        self.assertFalse(result)


class TestProjectManagement(unittest.TestCase):

    def setUp(self):
        # Create a temporary projects file
        self.projects_file = 'test_projects.json'
        # Mocking the logger to avoid file creation
        patch('main.logger').start()

    def tearDown(self):
        # Remove the temporary files after tests
        if os.path.exists(self.projects_file):
            os.remove(self.projects_file)
        patch.stopall()

    def test_01_load_projects(self):
        print("Running test 01: test_load_projects")
        with open(self.projects_file, 'w') as file:
            json.dump({}, file)
        projects = load_projects(self.projects_file)
        self.assertEqual(projects, {})

    def test_02_save_projects(self):
        print("Running test 02: test_save_projects")
        projects = {'proj1': {'title': 'Project 1', 'leader': 'leader1'}}
        save_projects(self.projects_file, projects)
        with open(self.projects_file, 'r') as file:
            loaded_projects = json.load(file)
        self.assertEqual(loaded_projects, projects)

    def test_03_create_project(self):
        print("Running test 03: test_create_project")
        projects = {}
        projects = create_project(projects, 'New Project', 'leader1')
        self.assertEqual(len(projects), 1)
        project_id = list(projects.keys())[0]
        self.assertEqual(projects[project_id]['title'], 'New Project')
        self.assertEqual(projects[project_id]['leader'], 'leader1')
def test_04_add_user_to_project(self):
        print("Running test 04: test_add_user_to_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        result = add_user_to_project(projects, project_id, 'user1')
        self.assertTrue(result)
        self.assertIn('user1', projects[project_id]['users'])

    def test_05_add_existing_user_to_project(self):
        print("Running test 05: test_add_existing_user_to_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        add_user_to_project(projects, project_id, 'user1')
        result = add_user_to_project(projects, project_id, 'user1')
        self.assertFalse(result)

    def test_06_remove_user_from_project(self):
        print("Running test 06: test_remove_user_from_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        add_user_to_project(projects, project_id, 'user1')
        result = remove_user_from_project(projects, project_id, 'user1')
        self.assertTrue(result)
        self.assertNotIn('user1', projects[project_id]['users'])

    def test_07_remove_nonexistent_user_from_project(self):
        print("Running test 07: test_remove_nonexistent_user_from_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        result = remove_user_from_project(projects, project_id, 'user1')
        self.assertFalse(result)

    def test_08_remove_task_from_project(self):
        print("Running test 08: test_remove_task_from_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        project = projects[project_id]
        with patch('builtins.input', side_effect=[
            'Task 1', 'Description 1', '2024-05-28', '2024-06-28', 'user1', 'High', 'ToDo', 'No comments'
        ]):
            add_task(project)
        task_id = list(project['tasks'].keys())[0]
        remove_task_from_project(project, task_id)
        self.assertEqual(len(project['tasks']), 0)

    def test_09_remove_nonexistent_task_from_project(self):
        print("Running test 09: test_remove_nonexistent_task_from_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        project = projects[project_id]
        with self.assertLogs('main.logger', level='WARNING') as log:
            remove_task_from_project(project, 'nonexistent_task_id')
        self.assertIn('Task ID not found.', log.output[-1])

    def test_10_remove_project(self):
        print("Running test 10: test_remove_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        remove_project(projects, project_id)
        self.assertEqual(len(projects), 0)

    def test_11_remove_nonexistent_project(self):
        print("Running test 11: test_remove_nonexistent_project")
        projects = create_project({}, 'New Project', 'leader1')
        with self.assertLogs('main.logger', level='WARNING') as log:
            remove_project(projects, 'nonexistent_project_id')
        self.assertIn('Project ID not found.', log.output[-1])

    def test_12_view_projects(self):
        print("Running test 12: test_view_projects")
        projects = create_project({}, 'New Project', 'leader1')
        with patch('builtins.input', return_value=''):
            with patch('rich.console.Console.print') as mock_print:
                view_projects(projects, 'leader1', 'user')
                mock_print.assert_called()

    def test_13_add_task(self):
        print("Running test 13: test_add_task")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        project = projects[project_id]
        with patch('builtins.input', side_effect=[
            'Task 1', 'Description 1', '2024-05-28', '2024-06-28', 'user1', 'High', 'ToDo', 'No comments'
        ]):
            add_task(project)
        self.assertEqual(len(project['tasks']), 1)
        task_id = list(project['tasks'].keys())[0]
        task = project['tasks'][task_id]
        self.assertEqual(task['title'], 'Task 1')

    def test_14_view_tasks_for_project(self):
        print("Running test 14: test_view_tasks_for_project")
        projects = create_project({}, 'New Project', 'leader1')
        project_id = list(projects.keys())[0]
        project = projects[project_id]
        with patch('builtins.input', side_effect=[
            'Task 1', 'Description 1', '2024-05-28', '2024-06-28', 'user1', 'High', 'ToDo', 'No comments'
        ]):
            add_task(project)
        with patch('rich.console.Console.print') as mock_print:
            view_tasks_for_project(project, 'leader1', 'user')
            mock_print.assert_called()

    def test_15_can_access_project(self):
        print("Running test 15: test_can_access_project")
        project = {
            'title': 'New Project',
            'leader': 'leader1',
            'users': ['user1'],
            'tasks': {}
        }
        self.assertTrue(can_access_project(project, 'leader1', 'user'))
        self.assertTrue(can_access_project(project, 'user1', 'user'))
        self.assertFalse(can_access_project(project, 'user2', 'user'))
        self.assertTrue(can_access_project(project, 'user2', 'admin'))

if __name__ == '__main__':
    unittest.main()
