# Bix-Voice-Assistant-for-desktop
Desktop-based Voice Controlled Automation System built using Python that performs system tasks such as opening applications, web searching, playing media, and controlling system settings through speech commands

🎙 Desktop Voice Controlled Automation System (Python)
📌 Overview

This project is a desktop-based voice assistant developed using Python.
It enables users to control various system functions using voice commands. The system integrates speech recognition and text-to-speech technologies to provide hands-free interaction with a Windows-based computer.

The assistant is designed for desktop automation and performs predefined system-level operations efficiently.

🚀 Features

Voice command recognition
Wake word activation
Open desktop applications
Perform Google searches
Play YouTube videos
Adjust system volume
Adjust screen brightness
Lock system
Shutdown and restart system
Voice switching (based on system availability)
Simple animated user interface

🛠 Technologies Used

Python 3.x
Speech Recognition
pyttsx3 (Offline Text-to-Speech Engine)
pyautogui
pywhatkit
webbrowser
os
subprocess
ctypes
screen_brightness_control
threading

⚙ How It Works

The system listens for a predefined wake word.
After activation, it captures the user’s voice command.
Speech input is converted into text.
The text is matched with predefined commands.
The corresponding system function is executed.
The assistant provides voice feedback.

💻 System Requirements
Windows 10 / 11
Python 3.10 or above
Microphone
Internet connection (required for YouTube and web search features)

⚠ Limitations
Internet required for online tasks.
Performance may reduce in noisy environments.
Supports predefined commands only.
Does not implement advanced natural language processing.

🔮 Future Improvements
Offline speech recognition integration
Multi-language support
Expanded command support
Improved graphical interface


## 🧠 Project Architecture

# Required python libraries:
pyttsx3
SpeechRecognition
pywhatkit
pyautogui
screen_brightness_control
pyaudio

The project is divided into two main Python modules:

### 1️⃣ voice_assistant.py
This file contains the core logic of the assistant:
- Handles speech recognition
- Detects wake word
- Processes user commands
- Executes system-level operations
- Controls assistant workflow

### 2️⃣ orbui.py
This file manages the graphical user interface:
- Creates animated ORB using Tkinter
- Displays assistant states (Listening, Speaking, Idle)
- Provides real-time visual feedback

### 🔄 How Both Files Work Together

- When the program starts, the ORB UI initializes first.
- The voice assistant module begins listening for commands.
- Based on assistant state (Listening / Speaking), the UI animation updates.
- The voice assistant sends signals to the ORB UI to change animation states.
- Together, they create a synchronized voice + visual interaction system.



