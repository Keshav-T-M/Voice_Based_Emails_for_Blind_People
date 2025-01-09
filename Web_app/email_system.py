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

def get_gmail_password():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for password...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        speak("Recognizing password...")
        password = recognizer.recognize_google(audio)
        password = password.replace(" ", "").replace("dot", ".").replace("at", "@").replace("hash", "#").replace(
            "dollar", "$").replace("percent", "%").replace("star", "*").replace("ampersand", "&").replace("underscore",
                                                                                                          "_").replace(
            "exclamation", "!")  # Replace spaces and convert "dot" to '.' and "at" to '@'
        speak(f"You said password: {password}")
        print(f"You said password: {password}")
        return password
    except Exception as e:
        print(e)
        return ""

def main(email, password, server):
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login(email, password)
    while True:
        speak("You can compose an email or logout. Say your choice.")
        command = listen()  # Get user command via speech
        if "compose" in command:
            speak("Composing email. Please provide recipient, subject, and body.")
            compose_email(server, email, password)
        elif "inbox" in command:
            speak("Accessing inbox.")
            access_inbox(server, email, password)
        elif "logout" in command:
            speak("Logging out. Goodbye!")
            server.logout()  # Logout from the email server
            break
        else:
            speak("Invalid command. Please try again.")

def convert_spoken_number_to_int(spoken_number):
    # Define a dictionary to map spoken numbers to their integer equivalents
    number_mapping = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        # Add more mappings as needed
    }
    try:
        # Try to convert the spoken number directly to an integer
        return int(spoken_number)
    except ValueError:
        # If conversion fails, try to map the spoken number to its integer equivalent
        spoken_number_lower = spoken_number.lower()
        return number_mapping.get(spoken_number_lower, None)

def compose_email(server, email, password):
    try:
        # accepting recipient's email address
        speak("You choose to compose an email")
        print("Composing an email:")
        speak("What is the recipient's email address? ")
        recipient = get_gmail_address()
        speak(f"Recipient's email address: {recipient}")
        print(f"Recipient's email address: {recipient}")
        # Get the subject of the email
        speak("What is the subject of the email? ")
        subject = recognize_speech()
        speak(f"Subject: {subject}")
        print(f"Subject: {subject}")
        # Get the body of the email
        speak("What is the body of the email? ")
        body = recognize_speech()
        speak(f"Body: {body}")
        print(f"Body: {body}")

        # Create the email message
        message = MIMEMultipart()
        message['From'] = email
        message['To'] = recipient

        message['Subject'] = subject

        body_text = MIMEText(body, 'plain')
        message.attach(body_text)

        speak("Do you want to add an audio attachment to the email? for 'yes' say accept  and for 'no' say n ")
        print("Do you want to add an audio attachment to the email? for 'yes' say accept  and for 'no' say n ")
        audio_attachment = recognize_speech()
        if "accept" in audio_attachment:
            speak("Please speak the content for the audio attachment: ")
            audio_content = recognize_speech()

            audio_file_path = "audio_attachment.wav"
            tts = gTTS(audio_content, lang='en')
            tts.save(audio_file_path)

            with open(audio_file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {audio_file_path}")

            # Adding audio file
            message.attach(part)
            speak("Audio attachment added successfully!")
            print("Audio attachment added successfully!")

        else:
            speak("No audio attachment requested.")
            print("No audio attachment requested !!!")

        text = message.as_string()

        # Send the email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.sendmail(email, recipient, text)
        server.quit()

        speak("Email sent successfully!")
        print("Email sent successfully!")

    except Exception as e:
        speak("Error sending email:")
        print("Error sending email:", str(e))

def access_inbox(server, email, password):
    try:
        # Access the inbox
        print("Accessing the Inbox")
        server.select("INBOX")

        # Get the count of unseen emails
        status, response = server.search(None, 'UNSEEN')
        unseen_count = len(response[0].split())

        # Get the count of seen emails
        status, response = server.search(None, 'SEEN')
        seen_count = len(response[0].split())
        speak(f"There are {unseen_count} unseen emails and {seen_count} seen emails in the inbox.")
        print(f"There are {unseen_count} unseen emails and {seen_count} seen emails in the inbox.")

        while True:
            speak("\nChoose an option:")
            speak("Read unseen emails")
            speak("Read seen emails")
            speak("Exit")
            speak("say your choice: ")
            choice = listen()
            print("You choosen "+ choice)


if __name__ == "__main__":
    main()