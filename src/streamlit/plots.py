import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3
from collections import Counter
from nltk.corpus import stopwords
import re
import nltk
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
                    hover_data=['Comment', 'roberta_neg', 
                                'roberta_neu', 'roberta_pos'],  # Shows the comment & sentiments
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

def convert_alpha2_to_alpha3(alpha_2):
    if not isinstance(alpha_2, str) or alpha_2.lower() == 'unknown':
        return None
    try:
        country_name = country_alpha2_to_country_name(alpha_2)
        return country_name_to_country_alpha3(country_name)
    except Exception as e:
        print(f"Error converting country code {alpha_2}: {e}")
        return None

def preprocess_and_plot(results_df, search_term):
    # Convert country codes from Alpha-2 to Alpha-3
    results_df['Country_alpha3'] = results_df['Country'].apply(convert_alpha2_to_alpha3)
    
    # Convert sentiment scores to numeric, handling non-numeric values
    for col in ['roberta_neg', 'roberta_neu', 'roberta_pos']:
        results_df[col] = pd.to_numeric(results_df[col], errors='coerce')
    
    # Calculate average sentiment
    results_df['avg_sentiment'] = results_df.apply(
        lambda x: (-1 * x['roberta_neg']) + (0 * x['roberta_neu']) + (1 * x['roberta_pos']), axis=1
    )
    
    # Aggregate average sentiment by country
    country_sentiment = results_df.groupby('Country_alpha3')['avg_sentiment'].mean().reset_index()

    # Generate and return the choropleth map with a fixed scale for the color range
    fig = px.choropleth(country_sentiment,
                        locations="Country_alpha3",
                        color="avg_sentiment",
                        hover_name="Country_alpha3",
                        locationmode='ISO-3',
                        color_continuous_scale=px.colors.diverging.RdYlGn,
                        range_color=[-1, 1])  # Setting the color scale range from -1 to 1

    # Update layout properties
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(landcolor='black', showocean=True, oceancolor='rgba(0,0,0,0)'),
        title=dict(x=0.5, xanchor='center', font=dict(size=24, color='white')),
        coloraxis_colorbar=dict(title='Sentiment', tickfont=dict(color='white'), titlefont=dict(color='white'))
    )
    
    # Update additional properties for a consistent look
    fig.update_geos(bgcolor='rgba(0,0,0,0)')
    fig.update_traces(marker_line_width=0.1, marker_line_color='black')
    fig.update_annotations(font=dict(color='white'))

    return fig

def timeline_plot(results_df, search_term):
    results_df['PublishedAt'] = pd.to_datetime(results_df['PublishedAt'])
    data_sorted = results_df.sort_values('PublishedAt')
    daily_averages = data_sorted.groupby(data_sorted['PublishedAt'].dt.date).agg({
        'roberta_neg': 'mean',
        'roberta_neu': 'mean',
        'roberta_pos': 'mean'
    }).reset_index()

    # Convert 'PublishedAt' back to datetime for plotting
    daily_averages['PublishedAt'] = pd.to_datetime(daily_averages['PublishedAt'])

    # Create a new plot with daily averages
    fig = go.Figure()
    bar_width = 0.8

    # Add traces for sentiments with specified colors
    fig.add_trace(go.Bar(
        x=daily_averages['PublishedAt'], y=daily_averages['roberta_neg'],
        name='Negative', marker_color='red', width=bar_width
    ))
    fig.add_trace(go.Bar(
        x=daily_averages['PublishedAt'], y=daily_averages['roberta_neu'],
        name='Neutral', marker_color='yellow', width=bar_width  # Adjusted to yellow
    ))
    fig.add_trace(go.Bar(
        x=daily_averages['PublishedAt'], y=daily_averages['roberta_pos'],
        name='Positive', marker_color='green', width=bar_width  # Adjusted to green
    ))

    fig.update_layout(
        xaxis=dict(
            type='date',
            title='Date',
            tickformat='%b %Y'  # Display only the year & month
            
        ),
        yaxis_title='Average Sentiment Score',
        title_text=f'Daily Average Sentiment Scores - {search_term}',
        barmode='stack'
    )
    return fig

def country_share(results_df):
    country_counts = results_df['Country'].value_counts()

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=country_counts.index, values=country_counts.values, pull=[0.1 if i == country_counts.idxmax() else 0 for i in country_counts.index])])

    # Update the layout to add title and improve readability
    fig.update_layout(
        title_text='Country Distribution',
        title_font_size=20,
        legend_title='<b> Countries </b>',
        legend_title_font_size=14,
        legend_font_size=12
    )

    return fig