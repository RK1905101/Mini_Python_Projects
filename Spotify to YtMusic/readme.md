# Spotify to YtMusic

A simple Python tool to transfer your Spotify playlists to YouTube Music.

---

## Features

* List all your Spotify playlists.
* Select a playlist to transfer.
* Search songs on YouTube Music.
* Create a new YouTube Music playlist with the matched songs.

---

## Requirements

* Python 3.10+
* `spotipy`
* `ytmusicapi`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Create `creds.json`

Create a file named `creds.json` in the project root with your Spotify API credentials:

```json
{
    "SPOTIPY_CLIENT_ID": "your_spotify_client_id_here",
    "SPOTIPY_CLIENT_SECRET": "your_spotify_client_secret_here",
    "SPOTIPY_REDIRECT_URI": "http://127.0.0.1:8888/callback",
    "SCOPE": "user-library-read playlist-read-private"
}
```

Get your Spotify API credentials from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

### 2. Create `browser.json` for YouTube Music

`ytmusicapi` uses `browser.json` for authentication. You can generate it automatically or manually.

#### Automatic method:

```bash
ytmusicapi browser
```

#### Manual example of `browser.json`:

```json
{
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "authorization": "your_authorization_token_here",
    "content-encoding": "gzip",
    "content-type": "application/json",
    "cookie": "your_cookie_data_here",
    "origin": "https://music.youtube.com",
    "user-agent": "your_user_agent_here",
    "x-goog-authuser": "0",
    "x-youtube-client-name": "67",
    "x-youtube-client-version": "your_client_version_here"
}
```

For full instructions, check [ytmusicapi documentation](https://ytmusicapi.readthedocs.io/en/latest/setup.html).

### 4. Run the tool

```bash
python main.py
```

Follow the prompts to select your Spotify playlist and transfer it to YouTube Music.

---

## File Structure

```
Spotify-to-YtMusic/
│
├── browser.json        # YouTube Music authentication
├── creds.json          # Spotify API credentials
├── main.py             # Main Python script
├── requirements.txt    # Project dependencies
├── readme.md           # Project documentation
```

---

### requirements.txt

```
spotipy==2.23.0
ytmusicapi==0.21.0
```

---

### Notes

* Ensure both `creds.json` and `browser.json` are in the same directory as `main.py`.
* You need a valid Spotify Developer account and YouTube Music authentication to use this tool.

**Now you can easily run this project and transfer playlists from Spotify to YouTube Music.**