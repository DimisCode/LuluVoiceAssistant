import speech_recognition as sr
import pyaudio
import webbrowser
from time import ctime
import playsound
import os
import random
from gtts import gTTS
import time
from phue import Bridge

from ip import hue_bridge


def access_lights(hue_bridge):
    b = Bridge(hue_bridge)
    light_names_list = b.get_light_objects("name")
    return light_names_list

r = sr.Recognizer()

def record_audio(ask = False):
    with sr.Microphone(0) as source:
        if ask:
            lulu_speak(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            lulu_speak("Sorry, I did not get that")
        except sr.RequestError:
            lulu_speak("Sorry but the service is down")
        return voice_data

def lulu_speak(audio_string):

    tts = gTTS(text=audio_string, lang="en")
    r = random.randint(1, 10000000)
    audio_file = "audio-" + str(r) + ".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    if "what is your name" in voice_data:
        lulu_speak("My name is Lulu")

    if "what time is it" in voice_data:
        lulu_speak(ctime())

    if "search" in voice_data:
        search = record_audio("What do you want to search for ?")
        url = "https://google.com/search?q=" + search
        
        webbrowser.get().open(url)
        lulu_speak("Here is what I found for " + search)

    if "light" in voice_data:
        dim = record_audio("to choose the brightness say low or  middle or high")
        if dim == "low":
            lights = access_lights(hue_bridge)
            for light in lights:
                lights[light].on = True
                lights[light].brightness = 10
        elif dim == "middle":
            lights = access_lights(hue_bridge)
            for light in lights:
                lights[light].on = True
                lights[light].brightness = 125



                lulu_speak(f"The lights have been adjusted to {dim} you stupid fuck")


time.sleep(1)
lulu_speak("How can I help you ?")
while 1:
    voice_data = record_audio()
    respond(voice_data)