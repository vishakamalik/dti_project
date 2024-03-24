from requests_html import HTMLSession
from rake_nltk import Rake
import nltk;
nltk.download('punkt')
import nltk;
nltk.download('stopwords')

# def extract():
#     s = HTMLSession
#     url='https://www.musicradar.com/reviews/tech/akg-c214-172209'
#     response = s.get(url)
#     return response.html.find('div#article-body', first=True).text

r = Rake()

url='The Center for Maximum Potential Building Systems (Max Pot; founded in 1975 in Austin, Texas, by the American architect Pliny Fisk III) in the late 1980s joined with others to support an experimental agricultural community called Blueprint Farm, in Laredo, Tzexas. Its broader mission—with applications to any geographic location—was to study the correlations between living conditions, botanical life, the growing of food, and the economic-ecological imperatives of construction. This facility was built as an integrative prototype, recognizing that nature thrives on diversity. Fisk concluded that single-enterprise and one-crop territories are environmentally dysfunctional—meaning, for example, that all of a crops predators converge, natural defenses are overwhelmed, and chemical spraying to eliminate insects and weeds becomes mandatory. In every respect, Blueprint Farm stood for diversified and unpredictable community development. The crops were varied, and the buildings were constructed of steel gathered from abandoned oil rigs and combined with such enhancements as earth berms, sod roofs, and straw bales. Photovoltaic panels, evaporative cooling, and wind power were incorporated in this utopian demonstration of the symbiotic relationships between farming and green community standards.9'

# r = Rake(punctuations = [')','(',',',':','),',').','.'])
# r.extract_keywords_from_text(url.replace('(','').replace(')',''))

r.extract_keywords_from_text(url)

ranked_phrases_with_scores = r.get_ranked_phrases_with_scores()

# Create an empty list to store tuples of scores and phrases
data = []

# Iterate over the ranked phrases with scores
for score, phrase in ranked_phrases_with_scores:

    data.append((score, phrase))

def display_dataframe(data):
    # Print column headers
    print("score\tphrase")
    # Iterate over the list of tuples
    for score, phrase in data:
        print(f"{score}\t{phrase}")

# display_dataframe(data)

# ranked phrases with scores stored in a variable called data
# data = [(score1, phrase1), (score2, phrase2), ...]

filtered_data = []

# Iterate over the data
for score, phrase in data:
    if score > 3:
        filtered_data.append((score, phrase))

display_dataframe(filtered_data)

# keywords_rake = r.get_ranked_phrases()
# print(r.get_ranked_phrases_with_scores())