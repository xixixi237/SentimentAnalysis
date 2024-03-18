import pandas as pd
import os

files_to_explode = [
    'AMD','Andrew Tate', 'Antisemetism', 'Apple', 'Arsenal',
    'Ben Shapiro', 'Biden', 'Bitcoin',
    'Candace Owens', 'Charles Leclerc', 'Christianity', 'cls', 'Copilot', 'Crypto',
    'Data Science', 'Extremism', 'FC Porto', 'Gaza', 'Intel', 'iphone', 'islam',
    'Islamophobia', 'Israel', 'Jordan Peterson', 'Judaism', 'Justin Trudeau',
    'Kier Starmer', 'Labour', 'Lewis Hamilton', 'Liverpool FC', 'Manchester United',
    'Max Verstapen', 'Michael Gove', 'Microsoft', 'Netanyahu', 'Nvidia', 'Open AI',
    'Pixel 8', 'Putin', 'Rishi Sunak', 'Sadiq Khan', 'Samsung S24', 'Samsung',
    'Sora', 'Tesla', 'Tories', 'Trump', 'xAI Grok'
    ]


import pandas as pd
import os

for file_name in files_to_explode:

    results_path = f'./data/raw/Youtube/youtube_{file_name}_results.csv'
    comments_path = f'./data/raw/Youtube/youtube_{file_name}_results_with_comments.csv'

    # Ensure the file exists before attempting to read it
    if os.path.exists(results_path) and os.path.exists(comments_path):
        results_df = pd.read_csv(results_path)
        comments_df = pd.read_csv(comments_path)

        comments_expanded = comments_df.assign(Comments=comments_df['Comments'].str.split(', ')).explode('Comments')

        # Save the final DataFrame to a new CSV file
        comments_expanded.to_csv(f'./data/processed/Youtube/{file_name}_YT.csv', index=False)
    else:
        print(f"File not found for {file_name}")
