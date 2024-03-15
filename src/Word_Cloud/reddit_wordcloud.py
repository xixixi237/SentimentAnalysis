from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pandas as pd


search_term = 'Gaza'
# Load dataset
file_path = f'./data/raw/reddit_{search_term}_results_with_comments.csv'
data = pd.read_csv(file_path)
# Drop 'ID', 'Author', 'URL'
data = data.drop(data.columns[[1, 2, 3]], axis=1)



# Combine all your text data into a single string
text = ' '.join(data['Top_Comments'])

# Function to change the color of the text
def colorful_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 0, 255)]
    return f'rgb{colors[np.random.randint(0, len(colors))]}'

# Generate a word cloud image
wordcloud = WordCloud(background_color='black', width=1600, height=800, color_func=colorful_func).generate(text)

# Display the generated image:
# the matplotlib way:
plt.figure(figsize=(20,10)) # Double the image size
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
