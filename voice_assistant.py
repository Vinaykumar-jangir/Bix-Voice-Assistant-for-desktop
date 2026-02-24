from pydoc import text
import pyttsx3
import speech_recognition as sr
from speech_recognition import WaitTimeoutError
import pywhatkit
import webbrowser
import pyautogui
import time
import os
import ctypes
import screen_brightness_control as sbc
import threading
import orbui
import datetime
import subprocess


SYSTEM_APPS = {
    # Office
    "word": ["winword"],
    "excel": ["excel"],
    "powerpoint": ["powerpnt"],

    # Browsers
    "chrome": ["chrome"],
    "edge": ["msedge"],

    # System
    "settings": ["ms-settings:"],
    "calculator": ["calc"],
    "file explorer": ["explorer"],

    # Popular apps
    "spotify": ["spotify"],
    "whatsapp": ["whatsapp"],

    # Web apps
    "linkedin": ["https://www.linkedin.com"],
    "youtube": ["https://www.youtube.com"]
}



# ORB UI 
threading.Thread(target=orbui.create_orb, daemon=True).start()

#  VOICE 
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 150)

def set_voice(choice):
    choice = choice.lower().strip()

    female_keywords = ["female", "woman", "girl", "femail"]
    male_keywords = ["male", "man", "boy", "mail", "mael"]

    for word in female_keywords:
        if word in choice:
            if len(voices) > 1:
                engine.setProperty("voice", voices[1].id)
                speak("Voice changed to female")
            else:
                speak("Female voice is not available")
            return

    for word in male_keywords:
        if word in choice:
            engine.setProperty("voice", voices[0].id)
            speak("Voice changed to male")
            return

    speak("Please say male voice or female voice")


def speak(text):
    engine.say(text)
    engine.runAndWait()
def log(text):
    print(text)


#  LISTEN 
def listen(timeout=4, phrase_limit=6):
    r = sr.Recognizer()
    r.energy_threshold = 300
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        except WaitTimeoutError:
            return ""
    try:
        return r.recognize_google(audio, language="en-in").lower()
    except:
        return ""
    

def listen_again(prompt):
    speak(prompt)
    return listen()

#  WAKE WORD 
def wait_for_wake_word():
    print("Sleeping... Say 'hey bix")
    while True:
        if "hey bix" in listen():
            orbui.show_orb()
            speak("Yes")
            return

#  HELPERS 
def clean(text, words):
    for w in words:
        text = text.replace(w, "")
    return text.strip()


#  ACTIONS 
def open_app(app):
    log(f"[ACTION] Opening application: {app}")
    speak(f"Opening {app}")

    # Open Windows Search (more backend-like than Start menu)
    pyautogui.hotkey("win", "s")
    time.sleep(1.0)

    # Type app name quickly
    pyautogui.write(app, interval=0.05)
    time.sleep(0.8)

    # Launch app
    pyautogui.press("enter")

    
def google_search(query):
    speak(f"Searching Google for {query}")
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)



def extract_song_name(query):
    fillers = [
        "play", "song", "songs",
        "on youtube", "youtube",
        "please", "this", "that", "the"
    ]

    cleaned = query
    for f in fillers:
        cleaned = cleaned.replace(f, "")

    cleaned = cleaned.strip()

    # If only filler words were spoken
    if len(cleaned) <= 2:
        return ""

    return cleaned


#  SYSTEM 
def lock():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def screen_off():
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
    
def shutdown_system():
    speak("Shutting down the system")
    os.system("shutdown /s /f /t 5")

def restart_system():
    speak("Restarting the system")
    os.system("shutdown /r /f /t 5")


def volume_up():
    pyautogui.press("volumeup")

def volume_down():
    pyautogui.press("volumedown")

def mute():
    pyautogui.press("volumemute")

def bright_up():
    sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))

def bright_down():
    sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
    

def listen_with_retry():
    command = listen()

    if not command:
        speak("I didn't catch that. Please say it again.")
        command = listen()

    if command:
        log(f"[HEARD] {command}")

    return command


#  COMMAND ENGINE 
def execute(query):

    if not query:
        return

    query = query.lower().strip()

    #  PLAY (ABSOLUTE PRIORITY) 
    
    if "play" in query:

        song = extract_song_name(query)

        # If user said "play this song" etc.
        if not song:
            song = listen_again("Please tell me the song name")

        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("I did not receive the song name")

        return  #  NEVER GOOGLE

    
        #  GOOGLE SEARCH 
    if query.startswith("google"):
        search_query = clean(query, ["google", "search", "on", "please"])

        if not search_query:
            search_query = listen_again("What should I search on Google?")

        if search_query:
            google_search(search_query)

        return
    
    
        #  CHANGE VOICE (FINAL & ROBUST) 
    if "voice" in query or "male" in query or "female" in query or "mail" in query or "femail" in query:

        # If user already said male/female
        if any(word in query for word in ["male", "mail", "female", "femail"]):
            set_voice(query)
            return

        # If user only said "change voice"
        speak("Do you want male voice or female voice?")
        choice = listen_again("Say male voice or female voice")
        if choice:
            set_voice(choice)
        return




    #  OPEN (ABSOLUTE PRIORITY) 
    #  OPEN 
    if "open" in query:
        app = clean(query, ["open", "app", "application", "please", "the"])

        if not app:
            app = listen_again("Which application should I open?")

        if app:
            open_app(app)
        else:
            speak("Please tell me the application name")

        return

    #  SYSTEM 
    if "volume up" in query:
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Increasing volume")
        return

    if "volume down" in query:
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Decreasing volume")
        return

    if "mute" in query:
        pyautogui.press("volumemute")
        speak("Muted")
        return

    if "brightness up" in query:
        try:
            sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
        except:
            speak("Brightness not supported")
        return

    if "brightness down" in query:
        try:
            sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
        except:
            speak("Brightness not supported")
        return

    if "lock" in query:
        lock()
        return

    if "sleep" in query or "screen off" in query:
        screen_off()
        return
        #  SHUTDOWN & RESTART 
    if "shutdown" in query or "shut down" in query or "power off" in query:
        shutdown_system()
        return

    if "restart" in query or "reboot" in query:
        restart_system()
        return


   
    return




#  MAIN LOOP 
if __name__ == "__main__":
    speak("Bix is running")
    while True:
        wait_for_wake_word()

        command = listen_with_retry()

        if command:
            execute(command)
        else:
            speak("Sorry, I could not understand the command")

        orbui.hide_orb()
        time.sleep(1)

