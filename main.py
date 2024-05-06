import requests
import os
import json
import time
from typing import Annotated
from fastapi import Body, FastAPI, Header

transcription_endpoint = os.environ.get("TRANSCRIPTION_ENDPOINT", "https://southeastasia.api.cognitive.microsoft.com/speechtotext/v3.2_internal.1/syncTranscriptions")
audio_uri = os.environ.get("AUDIO_URI", "https://oppobatchasrblobstorage.blob.core.windows.net/audios/en/english_30mins.wav?sp=r&st=2024-04-24T04:09:39Z&se=2024-12-31T12:09:39Z&spr=https&sv=2022-11-02&sr=b&sig=2RW0PzhJ3BGAqSuQvLQ%2Fz5NWrKhXOWwoOTd2TdkQiug%3D")
locale = os.environ.get("LOCALE", "en-US")
delay_seconds = os.environ.get("DELAY_SECONDS", 45)
speech_service_key = os.environ.get("SPEECH_SERVICE_KEY")

app = FastAPI()

@app.post("/speechtotext/v3.2_internal.1/syncTranscriptions")
def transcript(payload = Body(...), ocp_apim_subscription_key: Annotated[str | None, Header()] = None):
    transcription_result = os.environ.get("TRANSCRIPTION_RESULT")
    if transcription_result is None:
        transcription_result = call_service()
        os.environ.set("TRANSCRIPTION_RESULT", transcription_result)
    else:
        time.sleep(delay_seconds)
    return transcription_result

def call_service():
    definition = {
        "inputLocales": [locale],
        "wordLevelTimestampsEnabled": True,
        "profanityFilterMode": "Masked",
        "channel": [0, 1]
    }

    with requests.get(audio_uri, stream=True) as resp:
        resp.raise_for_status()
        stream = resp.raw
        files = {
            'definition': (None, json.dumps(definition), 'application/json'),
            'audio': ("audio", stream, 'application/octet-stream')
        }
  
        headers = {'Ocp-Apim-Subscription-Key': speech_service_key}
        with requests.post(transcription_endpoint, files=files, headers=headers) as response:
            response.raise_for_status()
            return response.json()