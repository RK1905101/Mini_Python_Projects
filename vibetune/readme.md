# 🎵 VibeTune – Your Ultimate Discord Music Bot 🎧

**VibeTune** is a sleek, Python-powered Discord music bot that brings your server to life with seamless YouTube playback, easy queue management, and modern control features.

---

## 🚀 Features

- 🔊 Play music from YouTube (audio-only)
- 🎚️ Adjust volume (optional feature)
- 🎼 Queue multiple songs with live updates
- ⏯ Pause, resume, skip, or stop tracks
- 🌀 Loop current song or entire playlist
- 🎤 Slash command support (easy to use)
- ⚙️ Lightweight, customizable, open-source

---

## 📦 Requirements

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html)
- A Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
- Required Python packages listed below

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/anandku06/vibetune.git
cd vibetune
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your `.env` file

Create a `.env` file in the root folder with the following:

```env
DISCORD_TOKEN=your_bot_token_here
```

---

## ▶️ Usage

Start the bot using:

```bash
python bot.py
```

---

## 🎛️ Commands

| Command       | Description                    |
| ------------- | ------------------------------ |
| `!play <url>` | Streams a YouTube song         |
| `!pause`      | Pauses the current track       |
| `!resume`     | Resumes paused playback        |
| `!skip`       | Skips to the next song         |
| `!queue`      | Shows the current song queue   |
| `!nowplaying` | Displays the current song info |
| `!stop`       | Stops and clears the queue     |

> Want slash commands? Check the `/commands` folder and enable them in your bot setup.

---

## 📂 Project Structure

```
📁 vibetune/
├── bot.py
├── music/
│   ├── player.py
│   └── queue.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

Feel like adding more vibes to VibeTune? Fork the project, submit a pull request, and let’s make this the best open-source music bot together!

---

## 📄 License

MIT License © 2025 [Your Name](https://github.com/anandku06)

---

## 💌 Support

Loved VibeTune? Give it a ⭐ on GitHub, share it with friends, or [create an issue](https://github.com/anandku06/vibetune/issues) if you need help.

---

🎧 Let the vibes flow with **VibeTune**!
