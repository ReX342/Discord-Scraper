import sqlite3
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
    return urls_dict

@app.route('/')
def index():
    messages = get_comments()
    urls_dict = get_urls()
    return render_template('index.html', messages=messages, urls_dict=urls_dict)

@app.route('/comments')
def comments():
    messages = get_comments()
    return render_template('comments.html', messages=messages)

@app.route('/urls')
def urls():
    urls_dict = get_urls()
    return render_template('urls.html', urls_dict=urls_dict)

# route to display embedded Youtube videos
@app.route('/yt')
def yt():
    # connect to database
    conn = sqlite3.connect('messages.db')
    cursor = conn.execute("SELECT content FROM messages WHERE content LIKE 'https://youtu.be/%'")
    urls = [row[0] for row in cursor.fetchall()]
    # close the database connection
    conn.close()
    return render_template('yt.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
