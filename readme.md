# Project Management System

## Overview

This Project Management System is designed to streamline the management of projects, user accounts, and tasks. The system supports user registration and authentication, project creation, user assignments, task management, and administrative functions. It is built with Python and uses CSV and JSON files for data storage.

## Features

### User Management
- **User Registration**: New users can sign up with a unique username, password, and email address.
- **User Login**: Registered users can log in with their credentials.
- **Duplicate Prevention**: The system prevents duplicate user registrations.

### Project Management
- **Project Creation**: Users can create new projects with a title and a designated project leader.
- **User Assignment**: Users can be added to or removed from projects.
- **Project Viewing**: Users can view a list of all projects they have access to.

### Task Management
- **Task Addition**: Users can add tasks to projects, including details like title, description, deadlines, assignees, priority, status, and comments.
- **Task Removal**: Tasks can be removed from projects.
- **Task Viewing**: Users can view all tasks associated with a project.

### Administrative Functions
- **Admin Creation**: The system allows for the creation of an admin user with a username and password.
- **Data Purge**: Admins can purge all data (accounts and projects) from the system.

## Setup and Usage

### Prerequisites
- Python 3.x
- `pandas` library
- `argparse` library
- `unittest` library

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/project-management-system.git
   cd project-management-system
   ```

2. Install the required Python packages:
   ```bash
   pip install pandas
   ```







## Acknowledgements

Thank you to everyone who contributed to this project. Your feedback and support are greatly appreciated.

---

For more information, please refer to the project documentation or contact the project maintainers.
