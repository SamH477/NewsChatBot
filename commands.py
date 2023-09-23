#TODO create commands for the chat bot
from speech_rec import voice_recognition
from datetime import date, datetime
today = date.today()
time = datetime.now()

commands = ["hello", "what's the date?", "what time is it?"]

responses = {"hello": "Hi! How can I help you?", "what's the date?": today, "what time is it": time}

while True:
    command = voice_recognition()
    if (command == 'goodbye'):
        break
