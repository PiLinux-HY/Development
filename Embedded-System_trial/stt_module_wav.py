from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums #v1p1beta1은 api의 버전을 나타냄.

def transcribe_audio(audio_file_path):
    client = speech.SpeechClient()

    # 설정
    language_code = "ko-KR"
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    sample_rate_hertz = 44100

    # 오디오 파일 열기
    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = {"content": content}

    config = {
        "language_code": language_code,
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
    }

    # 음성 파일 변환 요청
    response = client.recognize(config=config, audio=audio)

    # 결과 처리
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# 음성 파일 경로 설정
audio_file_path = "path_to_your_audio_file.wav"

# 음성 파일 변환 실행
transcribe_audio(audio_file_path)
