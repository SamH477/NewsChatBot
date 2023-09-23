#TODO create commands for the chat bot
import speech_rec
from datetime import date, datetime
today = date.today()
time = datetime.now()
str_today = today.strftime("%Y-%m-%d")
str_time = time.strftime("%I:%M%p")

commands = ["hello", "what's the date", "what time is it"]

responses = {"hello": "Hi! How can I help you?", "what's the date": str_today, "what time is it": str_time}

while True:
    command = speech_rec.voice_recognition()
    for cmds in commands:
        if (cmds == command):
            print("chatbot: " + responses[cmds])
        if (command == 'goodbye'):
            break
