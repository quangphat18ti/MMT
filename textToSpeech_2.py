import requests
import wget
import os 
from time import sleep

API_KEYS = ["Wl9kEb1iCENTIOwZ9z4OxudeYr5KER60", 
            "Wl9kEb1iCENTIOwZ9z4OxudeYr5KER60"
        ]
n_API_KEYS = len(API_KEYS)

from urllib import request
def download(URL):
    check = 0
    while check == 0:
        try:
            response1 = wget.download(URL, "audio.wav")
            check = 1
        except:
            check = 0

def TextToSpeech2(input):
    if os.path.isfile('audio.wav'):
        os.remove('audio.wav')

    url = 'https://api.fpt.ai/hmi/tts/v5'

    index = 0    
    while index < n_API_KEYS:
        try:
            payload = input
            headers = {
                'api-key': 'Wl9kEb1iCENTIOwZ9z4OxudeYr5KER60',
                'speed': '-1',
                'voice': 'minhquang',
                'format': 'wav'
            }
            response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)
            break
        except:
            index+=1

    URL = response.text.split('"')[3]
    URL = URL.strip()
    print("URL=", URL)

    download(URL)

    # response1 = request.urlretrieve(URL, "audio.wav")
    # print("Download Successfully!")

# TextToSpeech2("Xin Chào. Mình là Phát Cu-Te mãi đỉnh!")