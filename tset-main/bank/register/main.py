import speech_recognition as sr
from gtts import gTTS
from word2number import w2n
import pygame
import random

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()

# Google Pay API Integration
def make_google_pay_payment(amount, recipient):
    speak(f"Processing payment of {amount} to {recipient} using Google Pay.")

# Text-to-Speech Function
import time

# Text-to-Speech Function
def speak(aud, a=False):
    tts = gTTS(text=aud, lang='en', slow=False)
    a=random.random()
    tts.save(f"{a}output.mp3")
    pygame.mixer.music.load(f"{a}output.mp3")
    pygame.mixer.music.play()

    # Add a delay to allow time for the audio to play
    pygame.time.delay(int(4* 1000) + 1000)

    # Stop playing audio before removing the file
    pygame.mixer.music.stop()

# Speech Recognition Function
def listen():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            speak("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)  # Set a timeout of 5 seconds
                speak("Recognizing...")
                command = recognizer.recognize_google(audio)
                speak("Command:", command)
                return command
            except sr.WaitTimeoutError:
                speak("Speech recognition timeout. No audio detected within 5 seconds. Please try again.")
            except sr.UnknownValueError:
                speak("Sorry, could not understand the audio. Please try again.")
            except sr.RequestError as e:
                speak(f"Unexpected error: {e}")
                return None

# Number Recognition Function
def get_numeric_input():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            speak("Say a number:")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            # Use Google Web Speech API to recognize the spoken number
            number_text = recognizer.recognize_google(audio)
            numeric_value = w2n.word_to_num(number_text)
            return numeric_value
        except sr.UnknownValueError:
            speak("Sorry, could not understand the audio. Please try again.")
        except sr.RequestError as e:
            speak(f"Error with the speech recognition service; {e}")
            return None
        except ValueError:
            speak("Sorry, could not convert the recognized text to a number. Please try again.")

def register():

        speak("Let's register your account. Please provide a username.", a=True)
        username = listen()
        if username:
            speak("Please provide a password.", a=True)
            password = listen()
            if password:
                speak("Please confirm your password.", a=True)
                confirm_password = listen()
                if confirm_password == password:
                    speak("comfirm password registered successfully.", a=True)
                    speak("comfirm register by saying register account.", a=True)
                    register_account=listen()
                    if register_account:
                        speak("Account registered successfully", a=True)
                        return username,password,confirm_password
                    else:
                        speak("Account not registered", a=True)

                else:
                    speak("Passwords do not match. Registration failed.", a=True)
        return None, None

def log_in():
    speak("Let's log into your account. Please provide a username.", a=True)
    username = listen()
    if username:
        speak("Please provide a password.", a=True)
        password = listen()
        if password:
            speak("you have successfully logged in to your account", a=True)
            return username,password    
        
# Main Voice-Controlled Google Pay Program
def voice_control_google_pay():
    speak("Welcome to Voice-Controlled payment bot. Please say a command.",a=True)

    while True:
        command = listen()

        if command:
            if "register" in command:
                reg=list(register())
            elif "login" in command:
                log=list(log_in())            
            
            if "send money" in command:
                speak("Sure, please specify the amount.",a=True)

                amount = get_numeric_input()

                if amount is not None:
                    speak(f"You want to send {amount}. Who is the recipient?",a=True)
                    recipient_command = listen()

                    if recipient_command:
                        recipient = recipient_command.strip()
                        make_google_pay_payment(amount, recipient)
                        speak(f"Payment of {amount} to {recipient} has been completed.",a=True)
                    else:
                        speak("Recipient not recognized. Please try again.",a=True)

            elif "exit" in command or "quit" in command:
                speak("Exiting Voice-Controlled Google Pay. Goodbye!",a=True)
                pygame.mixer.music.stop()  # Stop playing audio
                break

            else:
                speak("Command not recognized. Please try again.",a=True)

if __name__ == "_main_":
    voice_control_google_pay()
