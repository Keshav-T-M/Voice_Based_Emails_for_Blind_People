import imaplib
import smtplib
import email
import re
import speech_recognition as sr
import pyttsx3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from gtts import gTTS

def recognize_speech():
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source,duration=0.5)  # Adjust for ambient noise with shorter duration
                speak("Listening...")
                audio = recognizer.listen(source, timeout=5)  # Set a timeout for listening
            text = recognizer.recognize_google(audio, language="en-US", show_all=False)
            return text
        except sr.WaitTimeoutError:
            speak("Listening timeout. Please speak again.")
        except sr.UnknownValueError:
            speak("Could not understand audio. Please repeat your command.")
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return None


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    