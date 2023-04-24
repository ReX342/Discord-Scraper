import sqlite3
import random
import re
from urllib.parse import urlparse

from flask import Flask, render_template

app = Flask(__name__)

def get_comments():
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM messages WHERE content NOT LIKE 'http%'")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return messages

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

    # Randomize the domains and URLs
    randomized_domains = list(urls_dict.keys())
    random.shuffle(randomized_domains)
    randomized_urls_dict = {}
    for domain in randomized_domains:
        urls = urls_dict[domain]
        random.shuffle(urls)
        randomized_urls_dict[domain] = urls

    # Limit to 50 URLs
    for domain in randomized_urls_dict:
        randomized_urls_dict[domain] = randomized_urls_dict[domain][:50]

    return randomized_urls_dict

def get_youtube_video_url():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT content FROM messages WHERE content LIKE 'https://www.youtube.com/watch?v=%'")
    rows = c.fetchall()
    conn.close()
    if not rows:
        return None
    video_id = random.choice(rows)[0]
    return f"https://www.youtube.com/embed/{video_id.split('=')[-1]}"

def get_random_comments():
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM messages WHERE content NOT LIKE 'http%' ORDER BY RANDOM() LIMIT 10")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return messages

@app.route('/')
def index():
    messages = get_random_comments()
    yt_url = get_youtube_video_url()
    urls_dict = get_urls()
    return render_template('index.html', messages=messages, urls_dict=urls_dict, yt_url=yt_url)

@app.route('/comments')
def comments():
    messages = get_comments()
    return render_template('comments.html', messages=messages)

@app.route('/urls')
def urls():
    urls_dict = get_urls()
    return render_template('urls.html', urls_dict=urls_dict)

@app.route('/yt')
def yt():
    return render_template('yt.html', yt_url=get_youtube_video_url())

# Jinja2 filter for splitting a string into a list using a delimiter
def split_filter(s="", delimiter=","):
    if s:
        return s.split(delimiter)
    else:
        return ""

app.jinja_env.filters['split'] = split_filter

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
