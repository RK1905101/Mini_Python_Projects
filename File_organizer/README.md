# 🗂️ **Advanced File Organizer**

> ✨ *A smart Python script that keeps your directories neat and
> organized automatically!*

------------------------------------------------------------------------

## � **Requirements**

- **Python 3.6+** (uses pathlib and modern os features)
- **Standard Library Only** - No external dependencies required

------------------------------------------------------------------------

## �📂 **Project Structure**

```
File_organizer/
├── organizer.py      # Main script - Entry point for the application
├── functions.py      # Core functions (scanning, moving, cleanup logic)
├── CONST.py          # Configuration (file categories, month mappings)
└── README.md         # Documentation
```

### Module Descriptions

**`organizer.py`**
- User interaction and input validation
- Orchestrates the file organization workflow
- Handles logging setup and error reporting

**`functions.py`**
- `all_files_dirs()` - Recursive directory scanning with `os.scandir()`
- `type_dest()` - File type classification based on extension
- `final_dir()` - Destination path calculation (Category/Year/Month)
- `move()` - Safe file moving with duplicate handling
- `remove_empty_dirs()` - Empty directory cleanup
- `setup_logging()` - Logging configuration

**`CONST.py`**
- `CATEGORIES` - File extension to category mappings
- `MONTHS` - Month number to name mappings

------------------------------------------------------------------------

## ⚡ **Key Features**

-   🧭 **Category-Based Sorting**\
    Groups files into clean parent folders like **Images**,
    **Documents**, **Videos**, and **Audio**, instead of creating a
    folder for every file type.

-   🧠 **Intelligent Conflict Handling**\
    Automatically renames duplicate files safely.\
    For example, if `report.pdf` already exists, the new file becomes
    `report(1).pdf`.

-   ⚙️ **Easily Customizable**\
    Modify the category dictionary in `CONST.py` to fit your
    needs.

-   ⚡ **Efficient Performance**\
    Uses `os.scandir()` for high-performance recursive file scanning --- significantly faster than traditional methods for
    directories with **thousands of files** and subdirectories.

-   🔄 **Cross-Filesystem Support**\
    Handles file moves across different drives or mount points seamlessly.

-   🧹 **Automatic Cleanup**\
    Removes empty directories after organizing to keep your workspace tidy.

-   📝 **Comprehensive Logging**\
    Creates a detailed log file (`file_organizer.log`) tracking all operations.

------------------------------------------------------------------------

## � **Installation & Usage**

### Installation

1️⃣ **Clone the repository** (or download the files):

``` bash
git clone <repository-url>
cd File_organizer
```

2️⃣ **Verify Python installation** (Python 3.6+ required):

``` bash
python --version
# or
python3 --version
```

### Usage

3️⃣ **Run the organizer script**:

``` bash
python organizer.py
# or on some systems
python3 organizer.py
```

4️⃣ **Enter the directory path** when prompted:

``` bash
# Example paths:
C:\Users\YourUser\Downloads          # Windows
/Users/youruser/Downloads            # macOS
/home/username/Downloads             # Linux
```

### What Happens During Execution

The script performs the following operations:

1. **Scans** the target directory and all subdirectories recursively
2. **Categorizes** files based on their extensions (defined in `CONST.py`)
3. **Creates** organized folder structure: `Category/Year/Month/`
4. **Moves** files to their appropriate destinations
5. **Handles** duplicates by appending `(1)`, `(2)`, etc. to filenames
6. **Cleans up** empty directories left behind
7. **Logs** all operations to `file_organizer.log` in the target directory

> **Note:** Already organized files (inside category folders) are automatically skipped to prevent re-organization.

------------------------------------------------------------------------

## 📁 **Before & After Example**

### 🌀 Before:

    Downloads/
    ├── vacation.jpg
    ├── budget.xlsx
    ├── song.mp3
    ├── my_resume.pdf
    ├── funny_video.mp4

### 🌈 After:

    Downloads/
    ├── Images/
    │   └── 2025/
    │       └── June/
    │           └── vacation.jpg
    ├── Documents/
    │   └── 2025/
    │       └── October/
    │           ├── budget.xlsx
    │           └── my_resume.pdf
    ├── Audio/
    │   └── 2025/
    │       └── January/
    │           └── song.mp3
    ├── Video/
    │   └── 2025/
    │       └── October/
    │           └── funny_video.mp4
    └── file_organizer.log

------------------------------------------------------------------------

## 🧩 **Customize Categories**

You can easily modify the `CATEGORIES` dictionary in `CONST.py` to support your
preferred extensions:

``` python
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Scripts & Code": [".py", ".js", ".html", ".css", ".sh", ".java", ".cpp", ".c"],
    "Executables": [".exe", ".msi", ".dmg"],
}
```
Files whose extensions don't match any configured category will be moved into an "**Other**" directory.
Add, remove, or rename categories as needed --- the script will handle
the rest automatically. 🪄

------------------------------------------------------------------------

## 🪄 **Pro Tips**

-   🕒 Automate it using:
    -   **Windows Task Scheduler**
    -   **macOS Automator**
    -   **Linux Cron Jobs**
-   🧰 Keep a backup for safety on first run.
-   🧹 Run regularly to keep your folders clutter-free.

------------------------------------------------------------------------

## 📦 **Example Categories Table**

  Category                    Example Extensions
  --------------------------- -----------------------------------------
  🖼️ **Images**               .jpg, .png, .gif, .svg, .webp
  📄 **Documents**            .pdf, .docx, .xlsx, .txt, .ppt
  🎧 **Audio**                .mp3, .wav, .aac, .flac, .ogg
  🎬 **Video**                .mp4, .mkv, .mov, .avi, .wmv
  💾 **Archives**             .zip, .rar, .7z, .tar, .gz
  🧠 **Scripts & Code**       .py, .js, .html, .css, .sh, .java
  ⚙️ **Executables**          .exe, .msi, .dmg

------------------------------------------------------------------------

## 🧑‍💻 **Technical Implementation**

### Core Technologies

- **`os.scandir()`** → High-performance recursive directory scanning with cached file attributes
- **`shutil.move()`** → Safe file relocation with automatic cross-filesystem support (handles moves across different drives/mount points)
- **`os.walk()`** → Bottom-up directory traversal for empty directory cleanup
- **Path objects** → Type-safe file path handling with pathlib

### Smart Features

- **Intelligent duplicate handling** → Checks destination existence before moving and auto-renames conflicts (e.g., `file(1).ext`, `file(2).ext`)
- **Category folder skipping** → Prevents re-organizing already sorted files by skipping category directories during scan
- **Empty directory cleanup** → Recursively removes empty folders after organizing (bottom-up traversal to handle nested empties)
- **Permission-aware scanning** → Gracefully skips directories without read permissions
- **Comprehensive logging** → Tracks all operations, errors, and exceptions in `file_organizer.log`
- **Date-based organization** → Uses file creation time to organize into Year/Month subdirectories

### Why This Approach?

**`os.scandir()` for scanning:**
- ⚡ **~2-3x faster** than `os.listdir()` or traditional `os.walk()` for large directories
- 📊 Caches file stat information (type, size, timestamps) reducing redundant system calls
- 🎯 Returns `DirEntry` objects with efficient `is_file()` and `is_dir()` methods

**`os.walk()` for cleanup:**
- 🔄 Bottom-up traversal (`topdown=False`) ensures child directories are processed before parents
- ✅ Guarantees complete removal of nested empty directory structures
- 🛡️ Safe iteration while modifying directory tree

**`shutil.move()` for file operations:**
- 🔄 Automatically handles cross-filesystem moves (copy + delete when needed)
- 🛡️ More robust than `Path.rename()` which fails across mount points
- ✅ Works seamlessly with both Path objects and strings

------------------------------------------------------------------------

## 🧠 **Fun Fact**

> On average, people spend **5--10 minutes per day** cleaning their
> downloads folder.\
> This script saves you that time --- every single day! ⏳

------------------------------------------------------------------------

## 🤝 **Contributing**

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Potential Improvements

- Add configuration file support (JSON/YAML)
- Implement dry-run mode to preview changes
- Add GUI interface
- Support for custom date formats
- Multi-language support for month names
- Undo functionality with operation history

------------------------------------------------------------------------

## 📝 **License**

This project is open source and available for personal and commercial use.

------------------------------------------------------------------------

## 🏁 **Conclusion**

The **Advanced File Organizer** is a lightweight, efficient tool that keeps your workspace organized automatically. With no external dependencies and high performance through `os.scandir()`, it's perfect for both personal use and integration into larger workflows.

**Key Benefits:**
- ⚡ Fast performance with large file collections
- 🛡️ Safe file handling with duplicate protection
- 🔄 Cross-platform and cross-filesystem support
- 📝 Comprehensive logging for audit trails
- ⚙️ Highly customizable categories

> 💡 *Save time. Stay organized. Focus on what matters.*

------------------------------------------------------------------------

**Created with ❤️ and Python 🐍**
