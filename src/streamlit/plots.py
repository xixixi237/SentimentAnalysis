
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from collections import Counter
from nltk.corpus import stopwords
import re
import nltk
plt.style.use('ggplot')
stop_words = set(stopwords.words('english'))


def violin_plot(results_df, search_term):
    # Renaming the sentiment types
    results_df = results_df.rename(columns={
        'roberta_neg': 'Negative',
        'roberta_neu': 'Neutral',
        'roberta_pos': 'Positive'
    })
    
    # Melt it into a long format
    long_df = results_df.melt(value_vars=['Negative', 'Neutral', 'Positive'], 
                              var_name='Sentiment', value_name='Score')

    # Dictionary mapping sentiment types to specific colors
    color_map = {
        'Negative': 'red',  
        'Neutral': 'blue',  
        'Positive': 'green'  
    }

    # Create the violin plot using Plotly Express
    fig = px.violin(long_df, y='Score', color='Sentiment',
                    violinmode='overlay',
                    title=f'Distribution of Sentiment Scores for {search_term}',
                    color_discrete_map=color_map)  # Apply the custom color map

    # Update layout for aesthetics
    fig.update_layout(
        yaxis_title='Score',
        xaxis_title='Sentiment',
        template='plotly_white'
    )

    fig.update_xaxes(tickangle=45)

    return fig

def likes_post(results_df, search_term):
    max_likes = results_df['Likes_y'].max()
    fig = px.scatter(results_df, x='ID', y='Likes_y',
                    hover_data=['Comment'],  # Shows the comment text on hover
                    color='Title',  # Color-code by title
                    title=f'Likes per Comment for {search_term}')

    # Larger figure size
    fig.update_layout(
        yaxis_title="Likes per Comment",
        hovermode="closest",
        yaxis=dict(range=[0, max_likes + (0.1 * max_likes)]),
        showlegend=True, 
        height=1000,
        width=1000 
    )

    # Potentially hide overlapping x-axis labels
    fig.update_xaxes(tickmode='array',
                    tickvals=[],
                    ticktext=[])

    return fig

def word_plot(results_df, search_term):
    # Function to clean and split comments into words
    def clean_and_split(comment, search_term):
        # Remove the search term
        for term in search_term.split():
            comment = re.sub(r'\b' + term + r'\b', '', comment, flags=re.IGNORECASE)
        
        # Remove non-alphabetic characters and split into words
        words = re.sub("[^a-zA-Z]", " ", comment).lower().split()
    
        # Remove stopwords and words that are 2 characters or less
        words = [w for w in words if w not in stop_words and len(w) > 2]
        return words

    # Clean comments, split into words, flatten the list of lists, and count occurrences
    all_words = results_df['Comment'].dropna().astype(str).apply(lambda x: clean_and_split(x, search_term))
    flat_list = [word for sublist in all_words for word in sublist]
    word_counts = Counter(flat_list)

    # Get the most common words and their counts
    most_common_words = word_counts.most_common(40)

    # Separate the words and counts into two lists for plotting
    words, counts = zip(*most_common_words)

    # Create a bar plot
    fig = px.bar(y=words, x=counts, orientation='h', title=f"Top 40 Most Common Words in {search_term} Comments",
                labels={'x':'Frequency', 'y':'Words'},
                color=counts,  # Assigns a color based on the counts
                color_continuous_scale='plotly3')
    fig.update_layout(
        xaxis_tickangle=-45,
        width=600, 
        height=1000, 
        title=f'Top 40 Most Common Words in {search_term} Comments',
        xaxis_title='Frequency',
        yaxis_title='Words'
    )
    return fig
