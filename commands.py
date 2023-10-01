import speech_rec
from datetime import date, datetime
import api_config
import requests
import sys
import pycountry

sys.stdout.reconfigure(encoding='utf-8')

today = date.today()
time = datetime.now()
str_today = today.strftime("%Y-%m-%d") 
str_time = time.strftime("%I:%M%p")

commands = ["hello", "what's the date", "what time is it"]

responses = {"hello": "Hi! How can I help you?", "what's the date": str_today, "what time is it": str_time}

while True:
    command = speech_rec.voice_recognition()
    if (command == 'goodbye'):
            sys.exit()
    for cmds in commands:
        if (cmds == command):
            print("chatbot: " + responses[cmds])
        if command.startswith("what's the news for"):
    # Split the command into words and look for the country
            words = command.split()
            if len(words) >= 5:
                country_name = ' '.join(words[4:])
                try:
            # Use pycountry to search for the country name
                    country = pycountry.countries.search_fuzzy(country_name)
                    if country:
                        country_code = country[0].alpha_2
            # Rest of your code here...
        
                except LookupError:
                    print(f"chatbot: Could not find the country code for '{country}'")
                    continue  # Skip processing this command and continue the loop
 
            # Add your API key
            #add conditional statements to specify what country they want their news from
            url = f"http://api.mediastack.com/v1/news?access_key={api_config.api_key}&countries={country_code}"
            response = requests.get(url)

            # Debugging: Print the entire API response
            #print(response.text)

            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    news_articles = data["data"]
                    if news_articles:
                        news_info = "Here are the latest news articles:\n"
                        for article in news_articles:
                            title = article.get("title", "No Title")
                            source = article.get("source", "Unknown Source")
                            news_info += f"- {title} from {source}\n"
                        print("chatbot: " + news_info.encode('utf-8', 'ignore').decode('utf-8'))
                    else:
                        print("chatbot: No news articles found.")
                else:
                    print("chatbot: 'data' field not found in the API response.")
            else:
                print(f"chatbot: API request failed with status code {response.status_code}")






