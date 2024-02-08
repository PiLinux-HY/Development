from os import read
from xml.etree.ElementPath import _Callback
import pyaudio
import wave
import sys
import time

def play(address) : 
	CHUNK = 512

	wf = wave.open(address, 'rb')
				
	p = pyaudio.PyAudio()

	def callback(in_data, frame_count, time_info,status):
		out_data = wf.readframes(frame_count)
		return (out_data, pyaudio.paContinue)

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate= wf.getframerate(), output= True, stream_callback = callback)

	stream.start_stream()

	while stream.is_active():
		time.sleep(0.1)

	stream.stop_stream()
	stream.close()
	wf.close()

	p.terminate()
