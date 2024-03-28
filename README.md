# Sentiment Analysis Across Social Media Platforms.
Final Project for Developer Academy Bootcamp


## Setup and Installation

Make sure you have Python installed on your machine.

1. Clone this repository or download the ZIP file.
2. Open a terminal/command prompt and navigate to the project directory.
3. Create a virtual environment:
   - Windows: `python -m venv venv`
   - macOS/Linux: `python3 -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`

## Running the App

1. In the terminal/command prompt, ensure you're in the project directory and the virtual environment is activated.
2. Run the app: `streamlit run your_app.py`

Open your web browser and go to the address shown in the terminal (usually http://localhost:8501) to see the app.


## Setting Up API Keys

This application requires access to Google's Youtube API, and thus you need to obtain an API key to use it. Follow these steps to set up your environment:

1. Visit https://developers.google.com/youtube/v3 and follow the instructions to obtain your API key for the Youtube API.
2. Create a file named `.env` in the root directory of this project.
3. Inside the `.env` file, add the following line, replacing `Your_Api_Key` with the key you obtained:

    DEVELOPER_KEY=Your_Api_key 