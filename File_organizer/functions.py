from CONST import *


def all_files_dirs(directory):
    """Get all files in the given directory

    Args:
        directory (str): given directory

    Returns:
        list[Path]: list of files
    """
    all_files = []
    
    def scan_directory(directory):
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    # Skip category folders to avoid re-organizing already sorted files
                    if entry.is_dir(follow_symlinks=False):
                        # Check if this is a category folder at the root level
                        rel_path = Path(entry.path).relative_to(directory)
                        if rel_path.parts and ( rel_path.parts[0] in CATEGORIES.keys() or rel_path.parts[0] == "Other"):
                            continue
                        # Recursively scan subdirectories
                        scan_directory(entry.path)
                    elif entry.is_file(follow_symlinks=False):
                        all_files.append(Path(entry.path))
        except PermissionError:
            # Skip directories we don't have permission to read
            pass
    
    scan_directory(directory)
    return all_files

def type_dest(file):
    """Determine the destination folder based on file type
    Args:
        file (Path): given file
    Returns:
        str: destination folder name
    """
    for key, value in CATEGORIES.items():
        if file.suffix in value:
            return key
    return "Other"

def final_dir(file, mainDir):
    """Determine the final directory path for the file
    Args:
        file (Path): given file
        mainDir (Path): main directory
    Returns:
        Path: final directory path
    """
    destinationType = type_dest(file)
    details = os.stat(file)
    year = str(time.gmtime(details.st_ctime).tm_year)
    month = MONTHS[time.gmtime(details.st_ctime).tm_mon]
    return Path(mainDir)/destinationType/year/month

def move(file, destination):
    """Move the file to the destination directory
    Args:
        file (Path): given file
        destination (Path): destination directory
    """
    # Ensure destination directory exists
    os.makedirs(destination, exist_ok=True)
    dest_path = destination / file.name

    # If target exists, pick a new unique name like 'name(1).ext'
    if dest_path.exists():
        base = file.stem
        ext = file.suffix
        counter = 1
        new_name = f"{base}({counter}){ext}"
        new_path = destination / new_name
        while new_path.exists():
            counter += 1
            new_name = f"{base}({counter}){ext}"
            new_path = destination / new_name
        dest_path = new_path

    # Use shutil.move which handles cross-filesystem moves; Path objects work with it
    try:
        shutil.move(str(file), str(dest_path))
    except Exception as e:
        # Log and re-raise for higher-level handling
        logging.exception(f"Failed to move {file} to {dest_path}: {e}")

def remove_empty_dirs(directory):
    """
    Recursively removes empty directories in the given path.
    Goes from deepest nested directories up to avoid leaving empty parent directories.
    Args:
        directory (Path): given directory
    """
    try:
        for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
            # Skip directories that are in CATEGORIES
            if (Path(dirpath).relative_to(directory).parts and 
                Path(dirpath).relative_to(directory).parts[0] in CATEGORIES.keys()):
                continue
                
            # If directory is empty (no files and no subdirectories)
            if not filenames and not dirnames:
                try:
                    os.rmdir(dirpath)
                    logging.info(f"Removed empty directory: {dirpath}")
                except OSError as e:
                    logging.error(f"Failed to remove directory {dirpath}: {e}")
    except Exception as e:
        logging.exception(f"Error while removing empty directories: {e}")

def setup_logging(log_file):
    logging.basicConfig(filename=log_file,
                        filemode='w',
                        level=logging.INFO,
                        encoding='utf-8')

