import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic


def load_creds(path="creds.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing {path}")
    with open(path, "r") as file:
        return json.load(file)


def init_spotify(creds):
    CACHE_PATH = '.spotify_cache'
    auth_manager = SpotifyOAuth(
        client_id=creds["SPOTIPY_CLIENT_ID"],
        client_secret=creds["SPOTIPY_CLIENT_SECRET"],
        redirect_uri=creds["SPOTIPY_REDIRECT_URI"],
        scope=creds["SCOPE"],
        cache_path=CACHE_PATH,
        open_browser=False
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def init_ytmusic():
    if not os.path.exists("browser.json"):
        raise FileNotFoundError("Missing browser.json for YTMusic authentication.")
    return YTMusic("browser.json")


def list_playlists(sp):
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        results = sp.next(results) if results['next'] else None
    return playlists


def select_playlist(playlists):
    print("\nFetching Spotify playlists...")
    for i, playlist in enumerate(playlists, start=1):
        print(f"{i}. {playlist['name']} ({playlist['tracks']['total']} tracks)")
    while True:
        try:
            choice = int(input("\nEnter the playlist number: "))
            if 1 <= choice <= len(playlists):
                return playlists[choice - 1]
        except ValueError:
            pass
        print("Invalid input. Try again.")


def fetch_tracks(sp, playlist_id):
    print("Fetching tracks from playlist...")
    tracks = []
    results = sp.playlist_items(playlist_id)
    while results:
        tracks.extend(results['items'])
        results = sp.next(results) if results['next'] else None
    return [
        {
            'name': i['track']['name'],
            'artist': i['track']['artists'][0]['name']
        }
        for i in tracks if i.get('track')
    ]


def search_yt_song(ytmusic, name, artist):
    query = f"{name} {artist}"
    try:
        results = ytmusic.search(query, filter="songs")
        return results[0]['videoId'] if results else None
    except Exception as e:
        print(f"Error searching '{query}': {e}")
        return None


def create_yt_playlist(ytmusic, title, description, video_ids):
    try:
        playlist_id = ytmusic.create_playlist(title=title, description=description, video_ids=video_ids)
        return f"https://music.youtube.com/playlist?list={playlist_id}"
    except Exception as e:
        print(f"Error creating YouTube playlist: {e}")
        return None


def main():
    print("Loading credentials...")
    creds = load_creds()

    print("Authenticating Spotify and YouTube Music...\n")
    sp = init_spotify(creds)
    ytmusic = init_ytmusic()

    playlists = list_playlists(sp)
    selected = select_playlist(playlists)
    print(f"Selected playlist: {selected['name']}")

    tracks = fetch_tracks(sp, selected['id'])
    print(f"Found {len(tracks)} tracks.")

    video_ids = []
    for idx, track in enumerate(tracks, start=1):
        print(f"[{idx}/{len(tracks)}] Searching '{track['name']} - {track['artist']}'")
        video_id = search_yt_song(ytmusic, track['name'], track['artist'])
        if video_id:
            video_ids.append(video_id)
        else:
            print(f"No match found for '{track['name']}'")

    if not video_ids:
        print("No songs found on YouTube Music. Exiting.")
        return

    playlist_url = create_yt_playlist(ytmusic, selected['name'], "Transferred from Spotify", video_ids)
    if playlist_url:
        print(f"✅ Playlist created successfully: {playlist_url}")
    else:
        print("Failed to create YouTube playlist.")


if __name__ == "__main__":
    main()
