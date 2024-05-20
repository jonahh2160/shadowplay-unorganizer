# Import packages
import os, yaml, shutil, send2trash
from collections import deque

# Read config from file
print("Reading config file")
with open("unorganizer_config.yaml", "r") as stream:
    try:
        # Store config into a dict
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        # Print error
        print(exc)

# Set config variables
target_directory = config["target_directory"]
exempt_folders = config["exempt_folders"]

# Get the current directory and create some deques
current_directory = os.path.dirname(os.path.realpath(__file__))
file_queue = deque()
folder_queue = deque()

# If the target directory is the default or empty, set it to the current_directory
if target_directory == "/path/to/target/directory" or not target_directory:
    target_directory = current_directory
print("Target directory is", target_directory)

# Loop through the directory contents: delete empty folders and add folder contents to a queue
for folder in os.listdir(current_directory):
    if os.path.isdir(folder) and folder not in exempt_folders:
        # If the folder is empty, delete it
        if not os.listdir(folder):
            print("Deleting", folder)
            send2trash.send2trash(folder)
        # Otherwise, add the folder and its contents the folder_queue and the file_queue
        else:
            folder_queue.append(folder)
            current_folder = os.path.join(current_directory, folder)
            for file in os.listdir(current_folder):
                file_queue.append(os.path.join(current_folder, file))

# Move the files in the file_queue to the main directory
while file_queue:
    file = file_queue.popleft()
    print("Moving", os.path.basename(file))
    shutil.move(file, target_directory)

# Move the now emptied folders to the recycling bin
while folder_queue:
    folder = folder_queue.popleft()
    print("Deleting", folder)
    send2trash.send2trash(folder)
    
print("Done!")