import pyaudio
import wave

def recorder():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:    
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    sound_file = wave.open("output.wav","wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    # test


