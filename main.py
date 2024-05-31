
import json
import os
import uuid
import re
from enum import Enum
from datetime import datetime
from account import UserAccount
import pandas as pd
from rich.console import Console
from rich.table import Table
from loguru import logger

console = Console()
logger.add(".\\APelahishokr\\application.log", rotation="1 MB")




class TaskStatus(Enum):
    BACKLOG = "Backlog"
    TODO = "To Do"
    DOING = "Doing"
    DONE = "Done"
    ARCHIVED = "Archived"


class TaskPriority(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


def load_projects(filename):
    logger.info("Loading projects from {}", filename)
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning("Projects file not found, creating a new one.")
        return {}


def save_projects(filename, projects):
    logger.info("Saving projects to {}", filename)
    with open(filename, 'w') as file:
        json.dump(projects, file, indent=4)


def create_project(projects, title, leader):
    logger.info("Creating project: {} by leader: {}", title, leader)
    project_id = str(uuid.uuid4())
    projects[project_id] = {'title': title, 'leader': leader, 'users': [leader], 'tasks': {}}
    return projects


def add_user_to_project(projects, project_id, username):
    logger.info("Adding user: {} to project ID: {}", username, project_id)
    if username not in projects[project_id]['users']:
        projects[project_id]['users'].append(username)
        logger.info("User added successfully to project ID: {}", project_id)
        return True
    else:
        console.print("[bold yellow]Warning:[/bold yellow] User already has access to this project.")
        logger.warning("User already has access to project ID: {}", project_id)
        return False


def can_access_project(project, username, role):
    return username == project['leader'] or username in project['users'] or role == "admin"


def remove_user_from_project(projects, project_id, username):
    logger.info("Removing user: {} from project ID: {}", username, project_id)
    if username in projects[project_id]['users']:
        projects[project_id]['users'].remove(username)
        logger.info("User removed successfully from project ID: {}", project_id)
        return True
    else:
        console.print("[bold yellow]Warning:[/bold yellow] User not found in this project.")
        logger.warning("User not found in project ID: {}", project_id)
        return False


def remove_task_from_project(project, task_id):
    if task_id in project['tasks']:
        del project['tasks'][task_id]
        console.print("[bold green]Task removed successfully![/bold green]")
    else:
        console.print("[bold red]Error:[/bold red] Task ID not found.")


def remove_project(projects, project_id):
    if project_id in projects:
        del projects[project_id]
        console.print("[bold green]Project removed successfully![/bold green]")
    else:
        console.print("[bold red]Error:[/bold red] Project ID not found.")


def add_task(project):
    task_id = len(project['tasks']) + 1
    task_title = input("Enter task title: ")
    task_description = input("Enter task description: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    assigned_to = input("Enter comma-separated usernames assigned to this task: ").split(',')
    while True:
        try:
            priority=TaskPriority[ input("Enter task priority (Critical/High/Medium/Low): ").upper()].value
            break
        except ValueError:
            console.print("[bold red]Error:[/bold red] Invalid input.")
    while True:
        try:
            status = TaskStatus[input("Enter task status (Backlog/ToDo/Doing/Done/Archived): ").upper()].value
            break
        except ValueError:
            console.print("[bold red]Error:[/bold red] Invalid input.")
    comments = project["leader"]+": "+input("Enter comments for the task: ")

    task = {
        'title': task_title,
        'description': task_description,
        'start_date': start_date,
        'end_date': end_date,
        'assigned_to': assigned_to,
        'priority': priority,
        'status': status,
        'comments': comments,
        'hisotry' : []
    }
    project['tasks'][task_id] = task
    console.print("[bold green]Task added successfully![/bold green]")

def view_projects(projects, username, role):
    leader_projects = {idx: (pid,proj) for idx, (pid, proj) in enumerate(projects.items()) if proj['leader'] == username or role=="admin"}

    console.print("[bold cyan]Projects you are leading:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Index")
    table.add_column("Project ID")
    table.add_column("Title")
    table.add_column("Leader")
    i=0
    for  project_id, (id,project) in leader_projects.items():
        table.add_row(str(i), id, project['title'],project['leader'])
        i+=1

    console.print(table)

    while True:
        project_index = input("Enter the index of the Project you want to manage (or press Enter to go back): ")
        if not project_index:
            break

        if not project_index.isdigit() or  not (int(project_index)<i and -1<int(project_index)):
            console.print("[bold red]Error:[/bold red] Invalid index.")
            continue

        project_index = int(project_index)
        project_id, (id,project) = list(leader_projects.items())[project_index]
        print(project)
        manage_project(projects, id, project, username,role)
        save_projects(projects_file, projects)
def manage_project(projects, project_id, project, username,role):
    while True:
        console.print(f"\n[bold]Managing Project: {project['title']}[/bold]")
        console.print("1. [bold]Add User to Project[/bold]")
        console.print("2. [bold]Remove User from Project[/bold]")
        console.print("3. [bold]Add Task[/bold]")
        console.print("4. [bold]Manage Tasks[/bold]")
        console.print("5. [bold]Back to Projects[/bold]")

        choice = input("Enter your choice: ")

        if choice == '1':
            user_to_add = input("Enter the username to add: ")
            add_user_to_project(projects, project_id, user_to_add)
        elif choice == '2':
            user_to_remove = input("Enter the username to remove: ")
            remove_user_from_project(projects, project_id, user_to_remove)
        elif choice == '3':
            add_task(project)
        elif choice == '4':
            manage_tasks(project,username,role)
        elif choice == '5':
            break
        else:
            console.print("[bold red]Invalid choice.[/bold red] Please enter a valid option.")


def manage_tasks(project,username,role):
    while True:
        view_tasks_for_project(project, username,role)
        task_index = input("Enter the Task Index you want to manage (or press Enter to go back): ")
        if not task_index:
            break

        try:
            task_index = int(task_index)
            task_list = list(project['tasks'].items())
            if 0 <= task_index and task_index< len(task_list):
                task_id, task = task_list[task_index]
                print(0)
                view_task_history(task)

                if not (can_access_task(task, project['leader'], username, role) and username!=project['leader'] and role!='admin'):
                   update_task(task, project['leader'])
                else:
                    update_task_status_or_comment(task, username)
            else:
                console.print("[bold red]Error:[/bold red] Invalid task index.")
        except ValueError:
            console.print("[bold red]Error:[/bold red] Invalid input. Please enter a valid task index.")

def can_access_task(task, project_leader, username, role):
    return username == project_leader or username in task['assigned_to'] or role == "admin"

def update_task(task, username):
    while True:
        console.print(f"\n[bold]Updating Task: {task['title']}[/bold]")
        console.print("1. [bold]Title[/bold]")
        console.print("2. [bold]Description[/bold]")
        console.print("3. [bold]Start Date[/bold]")
        console.print("4. [bold]End Date[/bold]")
        console.print("5. [bold]Assigned Users[/bold]")
        console.print("6. [bold]Priority[/bold]")
        console.print("7. [bold]Status[/bold]")
        console.print("8. [bold]Comments[/bold]")
        console.print("9. [bold]Finish Update[/bold]")

        choice = input("Enter the number of the attribute you want to update (or '9' to finish): ")

        if choice == '1':
            task['title'] = input(f"Enter new title (leave blank to keep '{task['title']}'): ") or task['title']
            record_task_history(task, 'title', task['title'])
        elif choice == '2':
            task['description'] = input(f"Enter new description (leave blank to keep '{task['description']}'): ") or task['description']
            record_task_history(task, 'description', task['description'])
        elif choice == '3':
            task['start_date'] = input(f"Enter new start date (leave blank to keep '{task['start_date']}'): ") or task['start_date']
            record_task_history(task, 'start_date', task['start_date'])
        elif choice == '4':
            task['end_date'] = input(f"Enter new end date (leave blank to keep '{task['end_date']}'): ") or task['end_date']
            record_task_history(task, 'end_date', task['end_date'])
        elif choice == '5':
            new_assigned_to = input(f"Enter new assigned users (comma-separated, leave blank to keep '{', '.join(task['assigned_to'])}'): ").split(',')
            task['assigned_to']+=new_assigned_to
            record_task_history(task, 'assigned_to', ', '.join(task['assigned_to']))
        elif choice == '6':
            new_pr = input(f"Enter new priority (leave blank to keep '{task['priority']}'): ") or task['priority']
            try:
                task['priority']=TaskPriority[new_pr.upper()].value
            except ValueError:
                console.print("[bold red]Error:[/bold red] Invalid input.")
            record_task_history(task, 'priority', task['priority'])
        elif choice == '7':
            new_status = input(f"Enter new status (leave blank to keep '{task['status']}'): ") or task['status']
            try:
                task['status']=TaskPriority[new_status.upper()].value
            except ValueError:
                console.print("[bold red]Error:[/bold red] Invalid input.")
            record_task_history(task, 'status', new_status)
            task['status'] = new_status
        elif choice == '8':
            task['comments'] = input(f"Enter new comments (leave blank to keep '{task['comments']}'): ") or task['comments']
            record_task_history(task, 'comments', task['comments'])
        elif choice == '9':
            console.print("[bold green]Task update complete![/bold green]")
            break
        else:
            console.print("[bold red]Error:[/bold red] Invalid choice. Please enter a number between 1 and 9.")
