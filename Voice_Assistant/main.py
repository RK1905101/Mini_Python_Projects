import speech_recognition as sr
import webbrowser
import time
import musicLibrary
import winsound
import requests
from gtts import gTTS
import os
import playsound

recognizer = sr.Recognizer()
newsapi = "API_KEY"

def speak(text):
    print(f" Speaking: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        filename = "temp_voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f" TTS error: {e}")


def play_beep():
    winsound.Beep(1000, 200)

def processCommand(command):
    command = command.lower()
    print(f" Command: {command}")

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open github " in command:
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")



    elif command.startswith("play"):
      parts = command.split(" ")
      if len(parts) > 1:
                song = " ".join(parts[1:]).lower()  # normalize to lowercase

                # create a case-insensitive music dictionary lookup
                music_lower = {k.lower(): v for k, v in musicLibrary.music.items()}

                if song in music_lower:
                    speak(f"Playing {song}")
                    webbrowser.open(music_lower[song])
                else:
                    speak("Sorry, I don't have that song.")
      else:
                speak("Please tell me which song to play.")



    elif "news" in command:
        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}"
            )
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if not articles:
                    speak("No news found.")
                else:
                    speak("Here are the top BBC news headlines.")
                    for i, article in enumerate(articles, start=1):
                        title = article.get("title", "No title")
                        print(f"{i}. {title}")
                        speak(title)
                        time.sleep(0.3)  # small gap between headlines
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            print(f" Error fetching news: {e}")
            speak("There was a problem fetching the news.")


if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

            try:
                word = recognizer.recognize_google(audio)
                print(f" Heard: {word}")
            except sr.UnknownValueError:
                print(" Could not understand wake word")
                continue

            if word.lower() == "jarvis":
                print("Wake word detected.")
                time.sleep(0.2)
                play_beep()
                time.sleep(0.3)

                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for command")
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=5)

                try:
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
        except sr.WaitTimeoutError:
            continue
        except Exception as e:
            print(f" Error: {e}")