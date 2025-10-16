# 🗂️ **Advanced File Organizer**

> ✨ *A smart Python script that keeps your directories neat and
> organized automatically!*

------------------------------------------------------------------------

## ⚡ **Key Features**

-   🧭 **Category-Based Sorting**\
    Groups files into clean parent folders like **Images**,
    **Documents**, **Videos**, and **Audio**, instead of creating a
    folder for every file type.

-   🧠 **Intelligent Conflict Handling**\
    Automatically renames duplicate files safely.\
    For example, if `report.pdf` already exists, the new file becomes
    `report (1).pdf`.

-   ⚙️ **Easily Customizable**\
    Modify the category dictionary at the top of the script to fit your
    needs.

-   ⚡ **Efficient Performance**\
    Uses `os.scandir()` for faster file scanning --- ideal for
    directories with **thousands of files**.

------------------------------------------------------------------------

## 💻 **How to Use**

1️⃣ **Ensure Python is installed** on your system\
Run this command to verify:

``` bash
python --version
```

2️⃣ **Place** the `organizer.py` script in any directory.

3️⃣ **Run the script** from your terminal:

``` bash
python organizer.py
```

4️⃣ When prompted, **enter the full path** of the folder you want to
organize.\
Examples:

``` bash
C:\Users\YourUser\Downloads      # Windows
/Users/youruser/Downloads           # macOS/Linux
```

✅ The script will create folders by category and move the files
automatically.

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
    │   └── vacation.jpg
    ├── Documents/
    │   ├── budget.xlsx
    │   └── my_resume.pdf
    ├── Audio/
    │   └── song.mp3
    └── Video/
        └── funny_video.mp4

------------------------------------------------------------------------

## 🧩 **Customize Categories**

You can easily modify this dictionary in the script to support your
preferred extensions:

``` python
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav", ".aac"]
}
```

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

  Category            Example Extensions
  ------------------- -----------------------
  🖼️ **Images**       .jpg, .png, .gif
  📄 **Documents**    .pdf, .docx, .xlsx
  🎧 **Audio**        .mp3, .wav, .aac
  🎬 **Videos**       .mp4, .mkv, .mov
  💾 **Archives**     .zip, .rar, .7z
  🧠 **Code Files**   .py, .js, .html, .css

------------------------------------------------------------------------

## 🧑‍💻 **Behind the Scenes**

This project uses: - **os.scandir()** → Fast file iteration\
- **shutil.move()** → Safe file relocation\
- **Custom renaming logic** → Prevents overwriting conflicts

Each file is processed efficiently and categorized according to your
configuration.

------------------------------------------------------------------------

## 🧠 **Fun Fact**

> On average, people spend **5--10 minutes per day** cleaning their
> downloads folder.\
> This script saves you that time --- every single day! ⏳

------------------------------------------------------------------------

## 🏁 **Conclusion**

The **Advanced File Organizer** keeps your workspace organized and
efficient --- automatically.\
Say goodbye to clutter and hello to productivity! 💼

> 💡 *Save time. Stay organized. Focus on what matters.*

------------------------------------------------------------------------

**Created with ❤️ and Python 🐍**
