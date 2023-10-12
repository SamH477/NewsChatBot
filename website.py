from flask import Flask, render_template, request

import speech_recognition as sr
from datetime import date, datetime
import api_config
import requests
import sys
import pycountry

app = Flask(__name__, template_folder='style')

recognizer = sr.Recognizer()
mic = sr.Microphone()

today = date.today()
time = datetime.now()
str_today = today.strftime("%Y-%m-%d") 
str_time = time.strftime("%I:%M%p")

commands = ["hello", "what's the date", "what time is it"]
responses = {"hello": "Hi! How can I help you?", "what's the date": str_today, "what time is it": str_time}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio', methods=['POST'])
def process_audio():
    audio_data = request.form.get('audioData')
    # Process the audio data (you'll need to implement this)
    return jsonify({'response': 'Your response here'})


@app.route('/listen', methods=['POST'])
def listen():
    try:
        with mic as source:
            audio = recognizer.listen(source, timeout=10)  
            command = recognizer.recognize_google(audio).lower()
            print("You:", command)  # Add this line for debugging
            for cmds in commands:
                if cmds == command:
                    return responses[cmds]
        return "Unknown"  # Moved this here to handle unrecognized commands
    except sr.WaitTimeoutError:
        print("Timeout. No command recognized.")  # Add this line for debugging
        return "Timeout"
    except sr.UnknownValueError:
        print("I could not understand, please try again.")  # Add this line for debugging
        return "Unknown"

@app.route('/get_news/<country>', methods=['GET'])
def get_news(country):
    try:
        # Use pycountry to search for the country name
        country = pycountry.countries.search_fuzzy(country)
        if country:
            country_code = country[0].alpha_2
            url = f"http://api.mediastack.com/v1/news?access_key={api_config.api_key}&countries={country_code}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    news_articles = data["data"]
                    if news_articles:
                        news_info = "Here are the latest news articles:\n"
                        for article in news_articles:
                            title = article.get("title", "No Title")
                            source = article.get("source", "Unknown Source")
                            url = article.get("url", "No URL")
                            news_info += f"- {title} from {source} {url}\n"
                        return news_info
                    else:
                        return "No news articles found."
                else:
                    return "'data' field not found in the API response."
            else:
                return f"API request failed with status code {response.status_code}"
        else:
            return f"Could not find the country code for '{country_name}'"
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
