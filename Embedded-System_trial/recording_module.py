import pyaudio
import wave
import time

SAMPLE_RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1 # channels 1은 mono 2는 stereo 형식 2는 입체적 소리로 데이터 크기 영향 줌.
###44100번 * 16비트/8비트 *1채널 = 88200byte(==88.2kb) 데이터 저장

CHUNK = 512 #read 함수를 한 번 수행할 때마다 512개*16비트/8비트 = 1024byte씩 음성데이터
RECORD_SECONDS = 5 # 5초 동안 음성을 녹음.
WAVE_OUTPUT_FILENAME = 'output.wav'

p = pyaudio.PyAudio()

frames = []

def callback(in_data, frame_count, time_info, status):
	frames.append(in_data)
	return (None, pyaudio.paContinue)

stream = p.open(format = FORMAT, channels = CHANNELS, rate = SAMPLE_RATE, input = True, frames_per_buffer = CHUNK, stream_callback=callback)

print('Start to record the audio.')#오디오 재생

stream.start_stream()

cnt = 0
while stream.is_active():
	time.sleep(0.1)
	cnt += 1
	if cnt > RECORD_SECONDS * 10:
		break

print('Recording is finished') # 오디오 재생

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(SAMPLE_RATE)
wf.writeframes(b''.join(frames))
wf.close()
