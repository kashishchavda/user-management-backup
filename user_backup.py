#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

LOG_FILE = "logs.txt"

def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} : {message}\n")

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("❌ Command failed!")

def user_exists(username):
    return subprocess.run(["id", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def group_exists(group):
    return subprocess.run(["getent", "group", group], stdout=subprocess.DEVNULL).returncode == 0

# -----------------------------
# USER FUNCTIONS
# -----------------------------

def add_user():
    username = input("Enter username: ")
    if user_exists(username):
        print("User already exists!")
    else:
        run_command(["sudo", "useradd", "-m", username])
        run_command(["sudo", "passwd", username])
        print("✅ User created")
        log_action(f"User {username} created")

def delete_user():
    username = input("Enter username: ")
    if user_exists(username):
        run_command(["sudo", "userdel", "-r", username])
        print("✅ User deleted")
        log_action(f"User {username} deleted")
    else:
        print("User not found!")

def modify_user():
    username = input("Enter username: ")
    if user_exists(username):
        run_command(["sudo", "passwd", username])
        print("✅ Password updated")
        log_action(f"Password updated for {username}")
    else:
        print("User not found!")

# -----------------------------
# GROUP FUNCTIONS
# -----------------------------

def create_group():
    group = input("Enter group name: ")
    if group_exists(group):
        print("Group already exists!")
    else:
        run_command(["sudo", "groupadd", group])
        print("✅ Group created")
        log_action(f"Group {group} created")

def add_user_to_group():
    username = input("Enter username: ")
    group = input("Enter group name: ")

    if user_exists(username) and group_exists(group):
        run_command(["sudo", "usermod", "-aG", group, username])
        print("✅ User added to group")
        log_action(f"{username} added to {group}")
    else:
        print("User or group not found!")

# -----------------------------
# BACKUP FUNCTION
# -----------------------------

def backup_directory():
    directory = input("Enter directory to backup: ")
    destination = input("Enter backup destination: ")

    if not os.path.isdir(directory):
        print("Directory not found!")
        return

    os.makedirs(destination, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{destination}/backup_{timestamp}.tar.gz"

    run_command(["tar", "-czf", backup_file, directory])

    print(f"✅ Backup created: {backup_file}")
    log_action(f"Backup of {directory} → {backup_file}")

# -----------------------------
# MENU
# -----------------------------

def menu():
    while True:
        print("\n========= MENU =========")
        print("1. Add User")
        print("2. Delete User")
        print("3. Modify User Password")
        print("4. Create Group")
        print("5. Add User to Group")
        print("6. Backup Directory")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            modify_user()
        elif choice == "4":
            create_group()
        elif choice == "5":
            add_user_to_group()
        elif choice == "6":
            backup_directory()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
