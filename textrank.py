import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re;
def clean_text(text):
    """
    Removes HTML tags, JavaScript functions, punctuation marks,
    lowercase words, and removes stop words.
    """
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text(separator=' ')  # Remove HTML tags
    text = re.sub(r'[0-9]+', '', text)  # Remove numbers 
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in word_tokenize(text) if word not in stop_words]
    return tokens

def calculate_textrank_without_damping(url):
    """
    Fetches content from the URL, performs text cleaning,
    creates a co-occurrence dictionary, and calculates
    scores for individual keywords based on co-occurrence frequency.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
        content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from URL: {e}")
        return None

    cleaned_text = clean_text(content)

    # Create co-occurrence dictionary
    cooccurrence_dict = {}
    for i in range(len(cleaned_text)):
        current_word = cleaned_text[i]
        for word in cleaned_text[i+1:]:  # Consider words after current word
            if current_word not in cooccurrence_dict:
                cooccurrence_dict[current_word] = {}
            cooccurrence_dict[current_word][word] = cooccurrence_dict[current_word].get(word, 0) + 1

    # Calculate score for each keyword based on co-occurrence frequency sum
    keyword_scores = {word: sum(counts.values()) for word, counts in cooccurrence_dict.items()}

    return keyword_scores


# Example usage (replace with your desired URL)
url = "https://www.britannica.com/art/green-architecture"
keyword_scores = calculate_textrank_without_damping(url)

if keyword_scores:
    for keyword, score in keyword_scores.items():
        print(f"{score} {keyword}")
else:
    print("Error fetching or processing content from URL.")


