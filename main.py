import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import os
from gtts import gTTS
import pygame
from fuzzywuzzy import process

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "").strip()
        closest_match, confidence = process.extractOne(song, musicLibrary.music.keys())
        if confidence > 80:
            link = musicLibrary.music[closest_match]
            speak(f"Playing {closest_match}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    else:
        speak("I didn't understand that command.")

if __name__ == "__main__":
    speak("Your Khushi at your command...")
    while True:
        try:
            print("Listening for the wake word...")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            if word.lower() == "khushi":
                speak("Ya")
                with sr.Microphone() as source:
                    print("Khushi is active. Listening for your command...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    print(f"Recognized command: {command}")
                    if command.lower() == "stop":
                        speak("Goodbye!")
                        break
                    processCommand(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
