import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import dotenv
import os
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
import torch
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser(description="Perform sentiment analysis on YouTube comments.")
parser.add_argument("search_term", type=str, help="The search term used to fetch YouTube data.")
args = parser.parse_args()
search_term = args.search_term

df = pd.read_csv(f'./data/{search_term}_youtube.csv')
df['NewID'] = range(1, len(df) + 1)

# load model from huggingface
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
# Move the model to GPU
if torch.cuda.is_available():
    model.cuda()




def polarity_scores_roberta(batch_examples):
    # Tokenize the batch of input text
    encoded_batch = tokenizer(batch_examples, return_tensors='pt', padding=True, truncation=True, max_length=512)
    
    # Check if a GPU is available and move the encoded batch to GPU
    if torch.cuda.is_available():
        encoded_batch = {k: v.to('cuda') for k, v in encoded_batch.items()}
    
    # Perform the prediction
    with torch.no_grad():
        outputs = model(**encoded_batch)
    
    # Move the outputs back to CPU for further processing with NumPy
    scores = outputs.logits.detach().cpu().numpy()
    scores = softmax(scores, axis=1)

    print(f"Sentiments analysed..")
    return scores

def softmax(x, axis=None):
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / np.sum(e_x, axis=axis, keepdims=True)

batch_size = 256  # Define batch size

# Initialize results dictionary
res = {}

# Process the DataFrame in batches
for i in tqdm(range(0, len(df), batch_size), total=np.ceil(len(df)/batch_size)):
    batch_df = df.iloc[i:i+batch_size]
    texts = batch_df['Comment'].fillna("").astype(str).tolist()  # Handle missing values and ensure string type
    ids = batch_df['NewID'].tolist()
    
    # Compute RoBERTa scores in batch
    roberta_scores = polarity_scores_roberta(texts)
    
    # Populate the results dictionary with RoBERTa scores
    for idx, myid in enumerate(ids):
        roberta_result = {
            'roberta_neg': roberta_scores[idx][0],
            'roberta_neu': roberta_scores[idx][1],
            'roberta_pos': roberta_scores[idx][2],
        }
        res[myid] = roberta_result

results_df = pd.DataFrame(res).T
results_df = results_df.reset_index().rename(columns={'index':'NewID'})
results_df = results_df.merge(df, how='left')

results_df.to_csv(f"C:\Data Science\data\processed\Youtube\{search_term}_roberta.csv")
print(f"Sentiment saved to C:\Data Science\data\processed\Youtube\{search_term}_roberta.csv")