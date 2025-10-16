# Smart File Organizer

A small Python utility to organize files in a specified directory into categorized subfolders based on file extensions.

## Features

- Sorts files into categories: Images, Documents, Videos, Audios, Archives, Scripts, Others.
- Can run once or repeat at a user-defined interval.
- Creates category folders automatically if they don't exist.

## Requirements

- Python 3.6+
- No external dependencies; uses only Python standard library modules (`os`, `shutil`, `argparse`, `time`, `datetime`).

## Usage

Run the script with the required `--path` argument pointing to the directory you want to organize. Optionally use `--interval` to run the organizer repeatedly at a given number of minutes.

Example (run once):

```powershell
python smart_file_organizer.py --path "C:\Users\YourName\Downloads" --interval 0
```

Example (run every 10 minutes):

```powershell
python smart_file_organizer.py --path "C:\Users\YourName\Downloads" --interval 10
```

## Customization

- Edit `FILE_CATEGORIES` at the top of `smart_file_organizer.py` to add or change file extension mappings to categories.
- Add new categories for other extensions, or adjust existing lists.

## Behavior & Notes

- Files without a matching extension are moved to `Others`.
- Only files in the specified base directory are moved; subdirectories are not inspected.
- The script will print progress and errors to the console.
- Use Ctrl+C to stop the repeated run loop.

## License

This project includes code by Sangam Paudel. Use, modify, and distribute as you like.
