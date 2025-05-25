import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import time
import sys

# Initialize the voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Print available voices to select the appropriate one
for voice in voices:
    print(f"Voice ID: {voice.id} - Language: {voice.languages}")

# Set voice based on your preference (e.g., English US or other)
engine.setProperty('voice', voices[1].id)  # Adjust this index based on your available voices

# Function to speak audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to wish based on the time of the day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Boss!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")

    speak("How may I help you?")

# Function to take user command via microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')  # Change to the desired language (e.g., 'en-us' for US English)
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

# Function to send an email
def sendEmail(to, content):
    try:
        # Ensure environment variable for email password is set
        email_password = os.getenv("EMAIL_PASSWORD")  # Use environment variable for password
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', email_password)
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email.")

# Main program
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        # Exit condition
        if 'exit' in query or 'stop' in query:
            speak("Goodbye Boss!")
            sys.exit()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = r"D:\Music"
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("No songs found in the directory.")
            else:
                speak("Music directory not found.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "c:\\Users\\Sumit\\OneDrive\\Desktop\\Jarvis\\AI.py"
            if os.path.exists(codePath):
                os.startfile(codePath)
            else:
                speak("The file path does not exist.")

        elif 'how are you' in query or 'how are you doing' in query:
            speak("I am fine, how are you?")

        elif 'email to sumit' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "helloworld@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")
