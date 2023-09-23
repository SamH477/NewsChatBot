import speech_recognition as sr

#Speech Recognition Works for the Bot but Commands need to be added 

recognizer = sr.Recognizer()
mic = sr.Microphone()
def voice_recognition():
    with mic as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)  # Listen for up to 10 seconds
            command = recognizer.recognize_google(audio).lower()  # listens to speech using google's speech recognition api
            print("You:", command)
            return command
        except sr.WaitTimeoutError:
            print("Timeout. No command recognized.")
            return None
        except sr.UnknownValueError:
            print("I could not understand, please try again.")
            return None
        
