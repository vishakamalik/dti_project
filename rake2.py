import requests
from bs4 import BeautifulSoup
from rake_nltk import Rake
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import re;
def clean_text(text):
    """
    Removes HTML tags, JavaScript functions, punctuation marks,
    lowercase words, and removes stop words (optional).
    """
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text(separator=' ')  # Remove HTML tags
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()

    # stop_words = set(stopwords.words('english'))
    # tokens = [word for word in word_tokenize(text) if word not in stop_words]
    # return tokens

    return text

def extract_keywords_with_rake(url):
    """
    Fetches content from the URL, performs text cleaning,
    and uses RAKE for keyword extraction.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
        content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from URL: {e}")
        return None

    cleaned_text = clean_text(content)

    # Use RAKE for keyword extraction
    r = Rake()
    r.extract_keywords_from_text(cleaned_text)
    keyword_phrases = r.get_ranked_phrases_with_scores()  # Get phrases with scores

    return keyword_phrases

url = "https://www.britannica.com/art/green-architecture"
keywords = extract_keywords_with_rake(url)

if keywords:
    for phrase, score in keywords:
        print(f"{phrase} {score}")
else:
    print("Error fetching or processing content from URL.")
