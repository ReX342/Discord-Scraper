from flask import Flask, render_template
from countdown import countdown
import threading
import random
import sqlite3
from urllib.parse import urlparse

app = Flask(__name__)

# Function to get comments from database
def get_comments():
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM messages WHERE content NOT LIKE 'http%'")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return messages

# Function to get URLs from database
def get_urls():
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM messages WHERE content LIKE 'http%'")
    urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    urls_dict = {}
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain == "youtu.be":
            continue
        if domain not in urls_dict:
            urls_dict[domain] = []
        urls_dict[domain].append(url)
    # Randomize the order of domains
    domains = list(urls_dict.keys())
    random.shuffle(domains)
    urls_dict = {domain: urls_dict[domain] for domain in domains}
    return urls_dict

# Route for home page
@app.route('/')
def index():
    # Call the countdown function in a separate thread
    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()

    yt_url = get_youtube_video_url()
    messages = get_random_comments()
    urls_dict = get_urls()
    return render_template('index.html', messages=messages, urls_dict=urls_dict, yt_url=yt_url)

# Route for comments page
@app.route('/comments')
def comments():
    messages = get_comments()
    return render_template('comments.html', messages=messages)

# Route for URLs page
@app.route('/urls')
def urls():
    urls_dict = get_urls()
    return render_template('urls.html', urls_dict=urls_dict)

# Route for YouTube video page
@app.route('/yt')
def yt():
    return render_template('yt.html', yt_url=get_youtube_video_url())

# Function to get 10 random comments from database
def get_random_comments():
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM messages WHERE content NOT LIKE 'http%' ORDER BY RANDOM() LIMIT 10")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return messages

# Function to get a random YouTube video URL from database
def get_youtube_video_url():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT content FROM messages WHERE content LIKE 'https://youtu.be/%'")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return None

    video_id = random.choice(rows)[0]
    watch_url = video_id.replace("https://youtu.be/", "https://www.youtube.com/watch?v=")
    embed_url = watch_url.replace("watch?v=", "embed/")

    return embed_url

# Jinja2 filter for splitting a string by delimiter
def split_filter(s="", delimiter=","):
    if s:
        return s.split(delimiter)
    else:
        return ""

app.jinja_env.filters['split'] = split_filter


if __name__ == '__main__':
    app.run(debug=True)
