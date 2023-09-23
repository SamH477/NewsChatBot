#TODO create commands for the chat bot
import speech_rec
from datetime import date, datetime
import api_config
import requests

#date and time commands
today = date.today()
time = datetime.now()
str_today = today.strftime("%Y-%m-%d")
str_time = time.strftime("%I:%M%p")

commands = ["hello", "what's the date", "what time is it", "what's the news"]

responses = {"hello": "Hi! How can I help you?", "what's the date": str_today, "what time is it": str_time, "what's the news": "here's the news:"}

while True:
    command = speech_rec.voice_recognition()
    for cmds in commands:
        if (cmds == command):
            print("chatbot: " + responses[cmds])
            if (command == "what's the news"): 
                #add api key
                url = f"https://api.mediastack.com/v1/news?access_key=&limit=5"
                response = requests.get(url)
                data = response.json()
                if "data" in data:
                    news_articles = data["data"]
                    if news_articles:
                        news_info = "Here are the latest news articles:\n"
                        for article in news_articles:
                            title = article.get("title", "No Title")
                            source = article.get("source", "Unknown Source")
                            news_info += f"- {title} from {source}\n"
                    print("chatbot: " + news_info)
                else:
                    print("chatbot: No news articles found.")
        if (command == 'goodbye'):
            break
