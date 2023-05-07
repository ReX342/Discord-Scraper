from countdown import countdown
import threading
import random
import sqlite3
from urllib.parse import urlparse
from functools import wraps
import time
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response



app = Flask(__name__, static_url_path='/static')

#D20

@app.route('/d20')
def d20():
    return render_template('d20.html')

#Picture feature
@app.route('/pictures')
def pictures():
    conn = sqlite3.connect('tf.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attachments ORDER BY RANDOM() LIMIT 20')
    attachments = c.fetchall()
    conn.close()
    return render_template('pictures.html', attachments=attachments)

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


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
    cursor = conn.execute("SELECT content FROM messages WHERE content LIKE 'http%' ORDER BY RANDOM() LIMIT 500")
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
    # Get remaining time from countdown function
    #remaining_time = countdown()
    remaining_time = 60
    
    #random attachment
    conn = sqlite3.connect('tf.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attachments ORDER BY RANDOM() LIMIT 1')
    attachments = c.fetchall()
    conn.close()
    random_attachment = attachments

    return render_template('index.html', messages=messages, urls_dict=urls_dict, yt_url=yt_url, remaining_time=remaining_time, random_attachment=random_attachment, attachments=attachments)

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

# Function to get dreams from database
def get_dreams():
    with sqlite3.connect('messages.db') as conn:
        cursor = conn.execute("SELECT content FROM dreams")
        dreams = [row[0] for row in cursor.fetchall()]
    return dreams


@app.route('/dreams')
def dreams():
    yt_url = get_youtube_video_url()
    dreams = get_dreams()
    urls_dict = get_urls()
    # Get remaining time from countdown function
    #remaining_time = countdown()
    remaining_time = 60
    return render_template('dreams.html', dreams=dreams, urls_dict=urls_dict, yt_url=yt_url, remaining_time=remaining_time)


# Route for random dreams page
@app.route('/random_dreams')
def random_dreams():
    dreams = get_random_dreams(20)
    urls_dict = get_urls()
    return render_template('random_dreams.html', dreams=dreams, urls_dict=urls_dict)


# Function to get a specified number of random dreams from the database
def get_random_dreams(num_dreams):
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM dreams ORDER BY RANDOM() LIMIT ?", (num_dreams,))
    dreams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dreams



if __name__ == '__main__':
    app.run(debug=True)
