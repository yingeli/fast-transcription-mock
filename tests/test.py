import time
import requests
import json

#transcription_endpoint = "https://ftmock.azurewebsites.net/speechtotext/v3.2_internal.1/syncTranscriptions"
transcription_endpoint = "http://localhost:8000/speechtotext/v3.2_internal.1/syncTranscriptions"

def transcript(audio_uri, config, speech_service_key):
    with requests.get(audio_uri, stream=True) as resp:  
        # ensure the request was successful  
        resp.raise_for_status()

        stream = resp.raw
        files = {
            'definition': (None, json.dumps(config), 'application/json'),
            'audio': ("audio", stream, 'application/octet-stream')
        }
        headers = {'Ocp-Apim-Subscription-Key': speech_service_key}
        with requests.post(transcription_endpoint, files=files, headers=headers) as response:
            return response

audio_uri = "https://oppobatchasrblobstorage.blob.core.windows.net/audios/en/english_30mins.wav?sp=r&st=2024-04-24T04:09:39Z&se=2024-12-31T12:09:39Z&spr=https&sv=2022-11-02&sr=b&sig=2RW0PzhJ3BGAqSuQvLQ%2Fz5NWrKhXOWwoOTd2TdkQiug%3D"
locale = "en-US"
definition = {
    "inputLocales": [locale],
    "wordLevelTimestampsEnabled": True,
    "profanityFilterMode": "Masked",
    "channel": [0, 1]
}
key = "xxxxxxxx"
        
start_time = time.time()

response = transcript(audio_uri, definition, key) 

response.raise_for_status()
print("Response: {}".format(response))

json = response.json()
print("Response json: {}".format(json))

end_time = time.time()
elapsed_time = end_time - start_time
print("Time elapsed: {} secs".format(elapsed_time))