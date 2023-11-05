import requests
from bs4 import BeautifulSoup

# Define the URL of the website you want to scrape
url = 'https://example.com'

# Define the keywords you want to search for
keywords = []

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the text on the page (you can modify this to narrow down the search)
    all_text = soup.get_text()
    
    # Create a dictionary to store keyword counts
    keyword_counts = {keyword: all_text.lower().count(keyword.lower()) for keyword in keywords}
    
    # Loop through the keywords and print the counts
    for keyword, count in keyword_counts.items():
        print(f'Keyword "{keyword}" was found {count} times on the page.')
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)





