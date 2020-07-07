import wave, os, sys
from pyaudio import PyAudio,paInt16
from flask import Flask

app = Flask(__name__)

framerate=16000
NUM_SAMPLES=1024
channels=1
sampwidth=2
TIME=2
def save_wave_file(filename,data):
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

#def start(current):
def start():
#    os.close(sys.stderr.fileno())
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   #input_device_index=1,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<framerate/NUM_SAMPLES*TIME:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.')
        #current.logger.debug('.')
    save_wave_file('record.wav',my_buf)
    stream.close()

if __name__ == '__main__':
    start()
