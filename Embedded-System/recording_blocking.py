import RPI.GPIO as GPIO
import pyaudio
import wave

SAMPLE_RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1 # channels 1은 mono 2는 stereo 형식 2는 입체적 소리로 데이터 크기 영향 줌.
###44100번 * 16비트/8비트 *1채널 = 88200byte(==88.2kb) 데이터 저장

CHUNK = 512 #read 함수를 한 번 수행할 때마다 512개*16비트/8비트 = 1024byte씩 음성데이터
RECORD_SECONDS = 5 # 5초 동안 음성을 녹음.
WAVE_OUTPUT_FILENAME = “output.wav”

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT, channels = CHANNELS, rate = SAMPLE_RATE, input = True, frames_per_buffer = CHUNK)

print(“Start to record the audio.”) # 목적지를 말씀해주세요 녹음 출력

frames = []
for I in range(0, int(SAMPLE_RATE / CHUNK * RECORD_SECONDS)): #430번 동안 반복
	data = stream.read(CHUNK) #오디오 데이터를 읽어 data 변수로 받는다
	frames.append(data) frame 

print(“Recording is finished”)

stream.stop_stream() 
stream.close()
p.terminate() 

wf = wave.open(WAVE_OUTPUT_FILENAME, ‘wb’) # output.wav파일이 있을 시 
wf.setchannels(CHANNELS) # 녹음 파일 채널 개수 설정
wf.setsampwidth(p.get_sample_size(FORMAT)) # 오디오 데이터 하나의 크기를 설정
wf.setframerate(SAMPLE_RATE) # 1초당 표본 추출된 오디오 데이터 개수
wf.writeframes(b’’.join(frames)) #음성 데이터를 붙여 넣기
wf.close() #녹음 파일을 닫는다.
