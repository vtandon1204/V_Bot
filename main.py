import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import webbrowser
import openai
import numpy as np

from config import apikey
from online import find_my_id, search_on_google, search_on_wikipedia, youtube
from datetime import datetime
from decouple import config
from conv import random_text
from random import choice

# pyttsx3 converts the given text into speech

engine = pyttsx3.init('sapi5')
# sapi5 is microsoft speech api used for speech recognition
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# voices[0] --> male assistant voice
# voices[1] --> female assistant voice

USER = config('USER')
HOSTNAME = config('BOT')

listening = False


def start_listening():
    global listening
    listening = True
    print("Started Listening...")


def pause_listening():
    global listening
    listening = False
    print("Stopped Listening...")


keyboard.add_hotkey('ctrl+alt+v', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour

    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USER}")
    elif 16 <= hour < 21:
        speak(f"Good Evening {USER}")
    speak(f"I'm {HOSTNAME}. How may I assist you {USER}?")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        r.pause_threshold = 0.5  # this will wait for the user to complete (by default = 0.8)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        # speak(queri)
        # this will all the commands given by the user
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        elif 'open' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if (hour >= 21) or (hour < 6):
                speak("Good Night sir, take care!")
            else:
                speak("Have a good day sir!")
                exit()
    except Exception:
        speak("Sorry I couldn't understand, Can you please repeat?")
        queri = 'None'
    return queri

def say(text):
    os.system(f'say "{text}"')
    
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)
        
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


if __name__ == '__main__':
    # speak("Hi I'm your Virtual Assistant V Bot")
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            # speak(query)
            if "how are you" in query:
                speak("I'm absolutely fine sir. What about you?")
            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')
            elif "open camera" in query:
                speak("Opening camera")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "IP address" in query:
                ip_address = find_my_id()
                speak(f"Your I.P address is {ip_address}")
                print(f"Your I.P address is {ip_address}")

            elif "play youtube" in query:
                speak(f"What do you want to play on YouTube {USER}?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}?")
                query = take_command().lower()
                search_on_google(query)

            elif "open wikipedia" in query:
                speak(f"What do you want to search on wikipedia {USER}?")
                search = take_command().lower()
                result = search_on_wikipedia(search)
                speak(f"According to wikipedia, {result}")
                speak(f"i am printing on terminal")
                print(result)

            elif "the time" in query:
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Sir time is {hour} and {min} minutes")
            
            elif "open facetime" in query:
                os.system(f"open /System/Applications/FaceTime.app")
            
            elif "Using artificial intelligence".lower() in query.lower():
                ai(prompt=query)
                
            elif "reset chat".lower() in query.lower():
                chatStr = ""
                
            else:
                print("Chatting...")
                chat(query)
            websites = [["youtube", "https://www.youtube.com/"],
                        ["lms", "https://lms.thapar.edu/moodle/login/"],
                        ["g mail", "https://mail.google.com/mail/u/1/#inbox"],
                        ["striver", "https://takeuforward.org/"],
                        ["github", "https://github.com/"],
                        ["lead code", "https://leetcode.com/problemset/"],
                        ["twitter", "https://x.com/home?lang=en-in"]
                        ]
            for w in websites:
                if f"open {w[0]}" in query:
                    speak(f"Opening {w[0]}")
                    webbrowser.open(w[1])

            apps = [["edge",
                     "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"],
                    ["whatsapp",
                     "C:\\Program Files\\WindowsApps\\5319275A.WhatsAppDesktop_2.2422.7.0_x64__cv1g1gvanyjgm\\WhatsApp.exe"],
                    ["linkedin",
                     "C:\\Program Files\\WindowsApps\\7EE7776C.LinkedInforWindows_3.0.30.0_x64__w1wdnht996qgy\\LinkedIn.exe"],
                    ["vs code", "C:\\Users\\Vaibhav Tandon\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"]]

            for a in apps:
                if f"open {a[0]}" in query:
                    speak(f"Opening {a[0]}")
                    os.startfile(a[1])
