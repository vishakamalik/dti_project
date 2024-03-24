import requests
from bs4 import BeautifulSoup
import nltk
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re;
from rake2 import extract_keywords_with_ranks
from textrank import calculate_textrank_without_damping

def clean_text(text):
    """
    Removes HTML tags, JavaScript functions, punctuation marks,
    lowercase words, and removes stop words.
    """
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text(separator=' ')  # Remove HTML tags
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in word_tokenize(text) if word not in stop_words]
    return tokens

def extract_keywords_with_ranks(url):
    """
    Fetches content, cleans text, extracts keywords using RAKE and TextRank,
    calculates combined scores using the specified formula, and returns sorted keywords.
    """
    cleaned_text = clean_text(url)

    # RAKE keyword extraction
    rake = Rake()
    rake.extract_keywords_from_text(cleaned_text)
    rake_keywords = rake.get_ranked_phrases_with_scores()

    # TextRank keyword extraction
    textrank_keywords = calculate_textrank_without_damping(cleaned_text)

    # Combine scores 
    keywords_with_ranks = {}
    for phrase, rake_score in rake_keywords:
        if phrase in textrank_keywords:
            textrank_score = textrank_keywords[phrase]
            combined_score = 2 * (rake_score * textrank_score) / (rake_score + textrank_score)
            keywords_with_ranks[phrase] = combined_score

    # Sort keywords by combined score
    sorted_keywords = sorted(keywords_with_ranks.items(), key=lambda x: x[1], reverse=True)

    return sorted_keywords

# Example usage
url = "https://www.britannica.com/art/green-architecture"
keywords = extract_keywords_with_ranks(url)

for keyword, combined_score in keywords:
    print(f"Keyword: {keyword}, Combined Score: {combined_score:.4f}")  # Print 4 decimal places for scores
