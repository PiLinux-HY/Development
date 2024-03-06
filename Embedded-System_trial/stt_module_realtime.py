import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from micstream import MicrophoneStream

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key"

RATE = 44100
CHUNK = int(RATE/10)

def  listen_print_loop(responses):

    for response in responses:
        result = response.results[0]
        transcript = result.alternatives[0].transcript

        print(transcript)

        if u'종료' in transcript or u'그만' in transcript:
            print("종료합니다")
            break


client = speech.SpeechClient()
config = types.RecognitionConfig(encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=RATE,language_code = "ko-KR")
streaming_config = types.StreamingRecognitionConfig(config=config)

with MicrophoneStream(RATE, CHUNK) as stream:
    audio_generator = stream.generator()
    requests = (types.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
    responses = client.streaming_recognize(streaming_config, requests)

    listen_print_loop(responses)