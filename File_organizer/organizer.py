from functions import *

# Get directory path from user
dir = ""
while len(dir) <1:
    dir = input("Enter the path of the directory to organize: ")
    if len(dir) < 1:
        print("Invalid input. Please enter a valid directory path.")

# Organize files
DIRECTORY = Path(dir)
allFFiles = all_files_dirs(DIRECTORY) # Get all files in the directory and its subdirectories
if len(allFFiles) < 1:
    print("No files found. Exiting...") # Exit if no files found
else:
    setup_logging(DIRECTORY/"file_organizer.log")
    for file in allFFiles:
        destination = final_dir(file, DIRECTORY)
        try:   
            move(file, destination)
            logging.info(f"File {file.name} moved to {destination}")
        except PermissionError:
            print(file.name)
            pass

remove_empty_dirs(DIRECTORY)

