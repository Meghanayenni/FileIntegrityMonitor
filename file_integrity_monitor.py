import os
import hashlib
import json
from datetime import datetime

BASELINE_FILE = "baseline.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None


def create_baseline(folder_path):
    baseline = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file == BASELINE_FILE:
                continue

            file_hash = calculate_hash(file_path)

            if file_hash:
                baseline[file_path] = file_hash

    with open(BASELINE_FILE, "w") as file:
        json.dump(baseline, file, indent=4)

    print("Baseline created successfully.")
    print("Total files recorded:", len(baseline))


def check_integrity(folder_path):
    if not os.path.exists(BASELINE_FILE):
        print("Baseline not found. Please create baseline first.")
        return

    with open(BASELINE_FILE, "r") as file:
        old_baseline = json.load(file)

    current_baseline = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file == BASELINE_FILE:
                continue

            file_hash = calculate_hash(file_path)

            if file_hash:
                current_baseline[file_path] = file_hash

    modified_files = []
    new_files = []
    deleted_files = []

    for file_path in old_baseline:
        if file_path not in current_baseline:
            deleted_files.append(file_path)
        elif old_baseline[file_path] != current_baseline[file_path]:
            modified_files.append(file_path)

    for file_path in current_baseline:
        if file_path not in old_baseline:
            new_files.append(file_path)

    print("\nFile Integrity Report")
    print("---------------------")
    print("Scan Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not modified_files and not new_files and not deleted_files:
        print("No changes detected.")
    else:
        if modified_files:
            print("\nModified Files:")
            for file in modified_files:
                print("-", file)

        if new_files:
            print("\nNew Files:")
            for file in new_files:
                print("-", file)

        if deleted_files:
            print("\nDeleted Files:")
            for file in deleted_files:
                print("-", file)


def main():
    print("=" * 40)
    print("       File Integrity Monitor")
    print("=" * 40)

    folder_path = input("Enter folder path to monitor: ")

    if not os.path.exists(folder_path):
        print("Invalid folder path.")
        return

    while True:
        print("\n1. Create Baseline")
        print("2. Check File Integrity")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_baseline(folder_path)

        elif choice == "2":
            check_integrity(folder_path)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()