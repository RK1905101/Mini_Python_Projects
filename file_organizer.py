import os
import shutil

# Define common file type mappings (can be expanded)
FILE_TYPE_MAPPING = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv'],
    'Documents': ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.txt'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css', '.c', '.cpp', '.java']
}

def organize_files(directory_path):
    """Organizes files in a given directory into subfolders based on extension."""
    
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at {directory_path}")
        return

    print(f"Starting organization in: {directory_path}")
    files_processed = 0

    # Reverse the mapping for easy lookup: {'.ext': 'Folder Name'}
    extension_to_folder = {}
    for folder, extensions in FILE_TYPE_MAPPING.items():
        for ext in extensions:
            extension_to_folder[ext.lower()] = folder

    # Iterate through all items in the directory
    for item_name in os.listdir(directory_path):
        # Skip if it's a directory or the script itself
        if os.path.isdir(os.path.join(directory_path, item_name)) or item_name == 'file_organizer.py':
            continue

        file_path = os.path.join(directory_path, item_name)
        
        # Get the file extension
        _, file_extension = os.path.splitext(item_name)
        file_extension = file_extension.lower()

        # Determine the target folder name
        target_folder_name = extension_to_folder.get(file_extension, 'Others')
        
        # Create the full path for the new folder
        target_folder_path = os.path.join(directory_path, target_folder_name)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)

        # Move the file
        try:
            shutil.move(file_path, os.path.join(target_folder_path, item_name))
            print(f"Moved: {item_name} -> {target_folder_name}/")
            files_processed += 1
        except Exception as e:
            print(f"Error moving {item_name}: {e}")

    print(f"\nOrganization complete! Total files processed: {files_processed}")
    if files_processed == 0:
         print("Note: No files were moved. Ensure the script is run in the directory you want to clean up.")


if __name__ == "__main__":
    # Get the directory from the user, defaulting to the script's current directory
    # If the user doesn't provide input, current directory ('.') is used.
    target_dir = input("Enter the path to the directory to organize (or press Enter for current directory): ").strip()
    
    if not target_dir:
        # Use the directory where the script is being executed
        target_dir = os.getcwd() 

    organize_files(target_dir)