import streamlit as st
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax
from tqdm import tqdm
from search_term_fetch import search_term_fetch
from produce_sentiment import produce_sentiment




def main():
    st.title("YouTube Comment Sentiment Analysis")

    search_term = st.text_input("Enter a search term:", "")

    if st.button("Analyze"):
        if search_term:
            # Display a message while data is being fetched and analyzed
            with st.spinner('Fetching YouTube data and analyzing sentiment...'):
                try:
                    # Fetch YouTube data
                    search_term_fetch(search_term)
                    # Now perform sentiment analysis on the fetched data
                    analysis_results_df = produce_sentiment(search_term)
                    # Display results
                    st.write(f"Sentiment analysis results for '{search_term}':")
                    st.dataframe(analysis_results_df)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a valid search term.")

if __name__ == "__main__":
    main()
