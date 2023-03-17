import speech_recognition as sr
import subprocess
import os
import time
import contextlib
import wave
from multiprocessing import Pool
import tempfile
# obtain path to "english.wav" in the same folder as this script
from os import path

# use the audio file as the audio source
r = sr.Recognizer()
# global arr 

def add_silence(file_name):
    # print(file_name)
    temp_file = os.path.join(next(tempfile._get_candidate_names())+'temp.wav')
    subprocess.run('sox ./sl.wav '+file_name+' ./sl.wav '+file_name.split('/')[-1].replace('.wav','1.wav'),shell=True, check=True,executable='/bin/bash')
    
    return file_name.split('/')[-1].replace('.wav','1.wav')
def check_duration(filepath):
    with contextlib.closing(wave.open(filepath,'r')) as fs:
        frames = fs.getnframes()
        rate = fs.getframerate()
        duration = frames / float(rate)
        return(duration)
def asr_gg(filepath):
    
    # with sr.AudioFile(add_silence(filepath)) as source:
    with sr.AudioFile((filepath)) as source:
        audio = r.record(source)  # read the entire audio file
    # print(audio)
    # recognize speech using Sphinx


    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        temp = str(r.recognize_google(audio,language='vi-VN').lower())
        return temp
        
    except sr.UnknownValueError:
        # print(fil)
        print(filepath +" Google Speech Recognition could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))


# print(asr_gg('ttt.wav'))