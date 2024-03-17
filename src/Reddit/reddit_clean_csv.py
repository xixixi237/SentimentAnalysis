import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

search_term = ''
# Load dataset
file_path = f'./data/raw/Reddit/reddit_{search_term}_posts_comments.csv'
data = pd.read_csv(file_path)
# Drop 'ID', 'Author', 'URL'
data = data.drop(data.columns[[1, 2, 3]], axis=1)


# Download necessary NLTK resources
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Text cleaning function
def clean_text(text):
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    text = re.sub(r'\@\w+|\#','', text)
    # Remove punctuations
    text = re.sub(r'[^\w\s]', '', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = [lemmatizer.lemmatize(word) for word in filtered_text]
    # Join words to create cleaned text
    text = ' '.join(lemmatized_text)
    return text

# Clean 'Title' and 'Top_Comments' columns
data['Title'] = data['Title'].apply(clean_text)
data['Top_Comments'] = data['Top_Comments'].apply(clean_text)

cleaned_file_path = f'./data/processed/Reddit/cleaned_reddit_{search_term}.csv'
data.to_csv(cleaned_file_path, index=False)

cleaned_file_path
