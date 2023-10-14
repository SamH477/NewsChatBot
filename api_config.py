import requests

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '3102dede7401422dab6c17ee6ace14af' #add personal apikey here from https://mediastack.com/

# Define the base URL for the API
base_url = 'http://api.mediastack.com/v1/'

# Create a dictionary of query parameters
params = {
    'access_key': api_key,
    'limit': 5,  # Number of articles to retrieve
}

# Make a GET request to fetch news articles
response = requests.get(base_url + 'news', params=params)

# Check the response status code
if response.status_code == 200:
    data = response.json()
    # Handle the retrieved data here
    #print(data)
else:
    print('Error:', response.status_code)
