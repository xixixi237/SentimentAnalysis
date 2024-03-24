import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
from tqdm import tqdm

# Assuming dotenv and necessary environment setup is handled elsewhere if needed

def produce_sentiment(search_term):
    # Define the path for the CSV file
    csv_file_path = f'./data/{search_term}_youtube.csv'
    
    # Load the DataFrame
    df = pd.read_csv(csv_file_path)
    df['NewID'] = range(1, len(df) + 1)

    # Load the model and tokenizer
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    # Move the model to GPU if available
    if torch.cuda.is_available():
        model.cuda()

    # Define the polarity_scores_roberta function
    def polarity_scores_roberta(batch_examples):
        encoded_batch = tokenizer(batch_examples, return_tensors='pt', padding=True, truncation=True, max_length=512)
        
        if torch.cuda.is_available():
            encoded_batch = {k: v.to('cuda') for k, v in encoded_batch.items()}
        
        with torch.no_grad():
            outputs = model(**encoded_batch)
        
        scores = outputs.logits.detach().cpu().numpy()
        scores = softmax(scores, axis=1)
        return scores

    # Process the DataFrame in batches
    batch_size = 256  # Define batch size
    res = {}  # Initialize results dictionary

    for i in tqdm(range(0, len(df), batch_size), total=np.ceil(len(df)/batch_size)):
        batch_df = df.iloc[i:i+batch_size]
        texts = batch_df['Comment'].fillna("").astype(str).tolist()
        ids = batch_df['NewID'].tolist()
        
        roberta_scores = polarity_scores_roberta(texts)
        
        for idx, myid in enumerate(ids):
            roberta_result = {
                'roberta_neg': roberta_scores[idx][0],
                'roberta_neu': roberta_scores[idx][1],
                'roberta_pos': roberta_scores[idx][2],
            }
            res[myid] = roberta_result

    results_df = pd.DataFrame(res).T
    results_df = results_df.reset_index().rename(columns={'index': 'NewID'})
    results_df = results_df.merge(df, how='left')
    
    # Optionally save the results DataFrame to a CSV file
    output_csv_path = f"./data/processed/Youtube/{search_term}_roberta.csv"
    results_df.to_csv(output_csv_path, index=False)
    
    print(f"Sentiment saved to {output_csv_path}")
    return results_df
