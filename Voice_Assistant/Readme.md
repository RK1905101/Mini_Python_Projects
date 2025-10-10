# Project-Jarvis

🎙️ Jarvis - Voice-Activated Virtual Assistant

Jarvis is a **voice-activated AI assistant** built in Python. It can recognize voice commands, respond with speech, open websites, play music, and fetch the latest news headlines from BBC.

This project is perfect for learning **speech recognition, text-to-speech, APIs, and Python automation**.


✨ Features

🎧 **Wake Word Activation**

  * Listens for the wake word `Jarvis` before processing commands.

 🗣 **Speech-to-Text & Text-to-Speech**

  * Uses `speech_recognition` to understand commands.
  * Responds using **Google Text-to-Speech (gTTS)** for a natural-sounding voice.


🌐 **Web Automation**

  * Opens popular websites:

    * `open google` → Opens Google
    * `open youtube` → Opens YouTube
    * `open github` → Opens GitHub


🎶 **Music Player**

  * `play <song name>` → Plays songs stored in `musicLibrary.py`.
  * Case-insensitive matching for song names.


📰 **News Headlines**

  * Fetches **BBC News** top headlines using [NewsAPI](https://newsapi.org/).
  * Reads them aloud with a small gap between each headline.


🔊 **Audio Feedback**

  * Plays a short beep when wake word is detected.

 
🛠️ Installation & Setup
## 1️⃣ Clone the Repository

git clone https://github.com/RameezHiro/Project-Jarvis
<br>
cd Project-Jarvis


## 2️⃣ Install Dependencies

Make sure you have **Python 3.8+** installed. Then install the required libraries:

pip install speechrecognition gtts playsound requests

> **Windows Users:** `winsound` is built-in and does not require installation.


## 3️⃣ Get Your NewsAPI Key

* Visit [https://newsapi.org/](https://newsapi.org/)
* Sign up for a free account and generate an API key.
* Replace the `newsapi` variable in the code with your key:

python
newsapi = "your_api_key_here"


## 4️⃣ Configure Your Music Library

Edit `musicLibrary.py` to add your favorite songs:

python
music = {
    "ncs": "https://www.youtube.com/watch?v=9iHM6X6uUH8",
    "neffex": "https://www.youtube.com/watch?v=24C8r8JupYY",
}


## ▶️ Usage

Run the assistant:

python jarvis.py

 **Step 1:** Jarvis will say *"Initializing Jarvis..."
 <br>
 **Step 2:** Speak the wake word **"Jarvis"**.
 <br>
 **Step 3:** Give a command, e.g.

  * **"Open Google"**
  * **"Play NCS"**
  * **"News"**

Jarvis will execute the task and respond with voice output.


## 📂 Project Structure

Voice-assistant/
<br>
├── main.py           # Main script
<br>
├── musicLibrary.py     # Dictionary with song names & links
<br>
├── README.md           # Documentation


## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it.