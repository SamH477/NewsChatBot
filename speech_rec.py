import speech_recognition as sr
import sys

recognizer = sr.Recognizer()

def voice_recognition(timeout=10):
    mic = sr.Microphone()  # Create microphone object
    with mic:
        try:
            audio = recognizer.listen(mic, timeout=timeout)  # Listen for up to 10 seconds
            command = recognizer.recognize_google(audio).lower()  # Listens to speech using Google's speech recognition API
            return command
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
