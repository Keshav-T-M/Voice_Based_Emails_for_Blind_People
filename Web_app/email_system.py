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

# def authenticate():
#     while True: 
#         # use your google app password ( it will be available at 2fa two factor authentication ) for google security purpose
#         email = input("Enter your Gmail address: ")
#         password = input("Enter your Gmail password: ")
#         try:
#             server = imaplib.IMAP4_SSL("imap.gmail.com")
#             server.login(email, password)
#             speak("Authentication successful!")
#             print("Authentication successful!")
#             return email,password,server
#         except Exception as e:
#             speak("Authentication failed: Please try again")
#             print("Authentication failed:", str(e))
#             return None

def authenticate():
    speak("Welcome to voice based email system.")
    speak("An innovative system designed for easy email management using voice commands.")
    while True:  # Keep looping until authentication succeeds
        # email = input("Enter your Gmail address: ")
        # password = input("Enter your Gmail password: ")

        email= get_gmail_address()
        speak("You said email address :" + email)
        print("Email Address:" + email)
        password = get_gmail_password()
        #speak("Listening for password...")
        #speak("Recognizing password...")
        # speak("You said Password :" + email)
        # print("You said Password:" + email)
        try:
            server = imaplib.IMAP4_SSL("imap.gmail.com")
            server.login(email, password)
            speak("Authentication successful!")
            print("Authentication successful!")
            return email, password, server
        except Exception as e:
            speak("Authentication failed: Please try again")
            print("Authentication failed:", str(e))
            print("Please try again.")
            
def listen():
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source,duration=0.5)  # Adjust for ambient noise with shorter duration
                speak("Listening...")
                audio = recognizer.listen(source, timeout=5)  # Set a timeout for listening
            text = recognizer.recognize_google(audio, language="en-US", show_all=False)
            text_without_spaces = re.sub(r'\s', '', text)
            text_lowercase = text_without_spaces.lower()
            speak(f"you said : {text_lowercase}")
            return text_lowercase
        except sr.WaitTimeoutError:
            speak("Listening timeout. Please speak again.")
        except sr.UnknownValueError:
            speak("Could not understand audio. Please repeat your command.")
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return None
def get_gmail_address():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            speak("Listening for email address...")
            print("Listening for email address...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            speak("Recognizing email address...")
            print("Recognizing email address...")
            email_address = recognizer.recognize_google(audio)
            email_address = email_address.replace(" ", "").replace("at", "@").replace("8", "@").replace("Gmail","gmail").replace("male", "mail").replace("dot", ".")  # Replace spaces and convert "at" to '@'
            if "@" not in email_address:
                speak("Sorry, I couldn't recognize the email address. Please try again.")
                continue
            else:
                speak(f"You said email address: {email_address}")
                # print(f"email address: {email_address}")
                return email_address
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't recognize the email address. Please try again.")
            continue

