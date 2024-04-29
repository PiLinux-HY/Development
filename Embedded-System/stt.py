# -*- coding: utf-8 -*-

from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment

# JSON 파일 경로
json_key_path = '/home/raspberrypi/Desktop/authentic-idea-416807-697117cb42c9.json'

# 서비스 계정 키를 사용하여 클라이언트 초기화
client = speech.SpeechClient.from_service_account_json(json_key_path)



# WAV 파일 경로
file_name = '/home/raspberrypi/Desktop/graduate_project_test_/output.wav'

def transcribe_audio():
    # 오디오 파일을 44100Hz에서 16000Hz로 변환
    audio = AudioSegment.from_wav(file_name).set_frame_rate(16000)
    converted_file_name = '/home/raspberrypi/Desktop/graduate_project_test_/output_16k.wav'
    audio.export(converted_file_name, format="wav")

    # WAV 파일을 모노 오디오로 변환
    sound = AudioSegment.from_wav(converted_file_name)
    sound = sound.set_channels(1)  # 모노 오디오로 변환
    sound.export(converted_file_name, format="wav")

    # 변환된 파일을 읽고 Google Cloud Speech API에 전달
    with open(converted_file_name, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR'
    )
    print("Execute")
    
    transcript_list = []
    
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print('Transcript:', result.alternatives[0].transcript)
        transcript_list.append(result.alternatives[0].transcript)
        
    transcript = "\n".join(transcript_list)
    return transcript
