import speech_rec
from datetime import date, datetime
import api_config
import requests
import sys
import pycountry
from flask import Flask, jsonify, render_template

app = Flask(__name__)

sys.stdout.reconfigure(encoding='utf-8')

today = date.today()
time = datetime.now()
str_today = today.strftime("%Y-%m-%d") 
str_time = time.strftime("%I:%M%p")

# Basic commands
commands = ["hello", "what's the date", "what time is it", "what's the news", "goodbye"]
# Basic responses
responses = {
    "hello": "Hi! How can I help you?",
    "what's the date": "Today is " + str_today,
    "what time is it": "It is " + str_time,
    "what's the news": "ask again and include a country",
    "goodbye": "see you later!"
}

@app.route('/')
def index():
    return render_template('index.html')

conversation_history = []

@app.route('/listen', methods=['POST'])
def listen():
    # Start voice recognition when the page loads
    command = speech_rec.voice_recognition()
    response = process_command(command)
    conversation_history.append({"user": command, "chatbot": response})
    return jsonify({"user": command, "chatbot": response})

def process_command(command):
    for cmds in commands:
        if cmds == command:
            return responses[cmds]
    if command and command.startswith("what's the news for"):
        words = command.split()
        if len(words) >= 5:
            country_name = ' '.join(words[4:])
            try:
                country = pycountry.countries.search_fuzzy(country_name)
                if country:
                    country_code = country[0].alpha_2
                # Rest of your code here...
            except LookupError:
                print(f"chatbot: Could not find the country code for '{country}'")

            url = f"http://api.mediastack.com/v1/news?access_key={api_config.api_key}&countries={country_code}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    news_articles = data["data"]
                    if news_articles:
                        news_info = news_info = "<ul>"  # Start an unordered list
                        for article in news_articles:
                            title = article.get("title", "No Title")
                            source = article.get("source", "Unknown Source")
                            url = article.get("url", "No URL")
                            news_info += f"<li><a href='{url}' target='_blank'>{title}</a> from {source}</li>"
                        news_info += "</ul>"
                        return "Here's the latest news for " + country_name + ":" + news_info
                    else:
                        return "No news articles found."
                else:
                    return "'data' field not found in the API response."
            else:
                return f"API request failed with status code {response.status_code}"
        else:
                return "Command not recognized. Please try again."

if __name__ == '__main__':
    app.run(debug=True, port=8001)