
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_instagram_hashtag(hashtag):
    # Get API key from environment variable
    api_key = '7336a24c94e137132ac65c275d7f7287'
    if not api_key:
        raise ValueError("SCRAPERAPI_KEY not found in environment variables")
    
    payload = {
        'api_key': api_key,
        'url': f'https://www.instagram.com/explore/tags/{hashtag}/',
        'render': 'true',  # Important for JavaScript-heavy sites
        'country_code': 'us',
        'premium': 'true'  # Use premium proxies if you have them
    }
    
    try:
        response = requests.get('https://api.scraperapi.com/', params=payload, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Save response to file for inspection
        with open('instagram_scrape.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print("Scraping completed. Data saved to instagram_scrape.html")
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"Error scraping Instagram: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    scrape_instagram_hashtag('grokai')