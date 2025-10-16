import os
import shutil
import time

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Scripts & Code": [".py", ".js", ".html", ".css", ".sh", ".java", ".cpp", ".c"],
    "Executables": [".exe", ".msi", ".dmg"],
}

def organize_files():
    path = input("Enter the path of the directory to organize: ")

    if not os.path.isdir(path):
        print("\nError: The specified path is not a valid directory. Please try again.")
        return

    try:
        print("\nScanning directory...")
        time.sleep(1)
        
        organized_count = 0
        
        with os.scandir(path) as entries:
            for entry in entries:
                if not entry.is_file() or "organizer" in entry.name:
                    continue
                
                file_path = entry.path
                file_name = entry.name
                file_extension = os.path.splitext(file_name)[1].lower()

                if file_name.startswith('.'):
                    continue

                target_folder_name = "Other"
                for category, extensions in CATEGORIES.items():
                    if file_extension in extensions:
                        target_folder_name = category
                        break
                
                target_folder_path = os.path.join(path, target_folder_name)

                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                    print(f"Created folder: '{target_folder_name}'")

                destination_path = os.path.join(target_folder_path, file_name)
                counter = 1
                while os.path.exists(destination_path):
                    name, ext = os.path.splitext(file_name)
                    destination_path = os.path.join(target_folder_path, f"{name} ({counter}){ext}")
                    counter += 1

                shutil.move(file_path, destination_path)
                print(f"Moved '{file_name}' -> '{target_folder_name}' folder.")
                organized_count += 1

        if organized_count == 0:
            print("\nNo new files were found to organize.")
        else:
            print(f"\nSuccess! Organized {organized_count} files.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    organize_files()

