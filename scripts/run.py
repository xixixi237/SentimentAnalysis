import subprocess

def run_script(script_name, search_term):
    subprocess.run(["python", script_name, search_term], check=True)

def main():
    search_term = input("Enter search term for sentiment analysis   ")  # Set your search term here
    scripts = [
        "./src/Youtube/youtube_fetch_posts.py",
        "./src/Reddit/reddit_fetch_posts.py",
        "./src/Youtube/youtube_fetch_comments.py"
        "./src/Reddit/reddit_fetch_comments.py"
    ]

    for script in scripts:
        run_script(script, search_term)

if __name__ == "__main__":
    main()