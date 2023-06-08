import pyaudio
import wave
import speech_recognition as sr

def speech_to_text():

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

def main():
    speech_to_text()
    
    r = sr.Recognizer()
    audio = sr.AudioFile("output.wav")
    with audio as source:
        audio = r.record(source)

    input = r.recognize_google(audio)
    print(type(input))

    with open("speech.txt" ,"w") as f:
        f.write(input)

main()

    # test


