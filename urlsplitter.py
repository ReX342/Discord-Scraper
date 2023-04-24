import sqlite3
import re
from flask import Flask, render_template

# create a Flask instance
app = Flask(__name__)

# define routes for each webpage
@app.route('/')
def index():
    urls, url_counts = get_urls()
    return render_template('index.html', urls=urls, url_counts=url_counts)

@app.route('/attachments')
def attachments():
    attachments = get_attachments()
    return render_template('attachments.html', attachments=attachments)

@app.route('/messages')
def messages():
    messages = get_messages()
    return render_template('messages.html', messages=messages)

# function to get all URLs from the content field
def get_urls():
    # connect to database
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # query for selecting content field
    query = "SELECT content FROM messages"

    # execute the query and fetch all rows
    c.execute(query)
    rows = c.fetchall()

    # initialize a list to store URLs and a dictionary to store URL counts
    urls = []
    url_counts = {}

    # iterate over rows and extract URLs from content field
    for row in rows:
        content = row[0]
        urls_in_content = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content)
        for url in urls_in_content:
            urls.append(url)
            if url in url_counts:
                url_counts[url] += 1
            else:
                url_counts[url] = 1

    # close the database connection
    conn.close()

    return urls, url_counts

# function to get all attachments from the content field
def get_attachments():
    # connect to database
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # query for selecting content field
    query = "SELECT content FROM messages"

    # execute the query and fetch all rows
    c.execute(query)
    rows = c.fetchall()

    # initialize a list to store attachments
    attachments = []

    # iterate over rows and extract attachments from content field
    for row in rows:
        content = row[0]
        if content.startswith('Attachment:'):
            attachments.append(content)

    # close the database connection
    conn.close()

    return attachments

# function to get all non-url comments and messages
def get_messages():
    # connect to database
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # query for selecting content field
    query = "SELECT content FROM messages"

    # execute the query and fetch all rows
    c.execute(query)
    rows = c.fetchall()

    # initialize a list to store messages
    messages = []

    # iterate over rows and extract messages from content field
    for row in rows:
        content = row[0]
        if not (content.startswith('http') or content.startswith('Attachment:')):
            messages.append(content)

    # close the database connection
    conn.close()

    return messages

# run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
