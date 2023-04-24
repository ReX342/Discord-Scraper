from flask import Flask, render_template
import sqlite3
import re
import tldextract
import sqlite3

conn = sqlite3.connect('messages.db')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# function to get all non-URL comments
def get_comments():
    # connect to database
    c = conn.cursor()

    # query for selecting content field where no URLs are present
    query = "SELECT content FROM messages WHERE content NOT LIKE 'URL%'"

    # execute the query and fetch all rows
    c.execute(query)
    rows = c.fetchall()

    # initialize a list to store all comments
    comments = []

    # iterate over rows and append comments to the list
    for row in rows:
        comments.append(row[0])

    return comments

# function to get all messages that start with 'http' and sort them by domain and path
def get_urls():
    # connect to database
    c = conn.cursor()

    # query for selecting content field where URLs are present
    query = "SELECT content FROM messages WHERE content LIKE 'http%'"

    # execute the query and fetch all rows
    c.execute(query)
    rows = c.fetchall()

    # initialize a dictionary to store URLs sorted by domain and path
    urls_dict = {}

    # iterate over rows and extract URLs from content field
    for row in rows:
        content = row[0]
        url = re.findall('(https?://[^\s]+)', content)[0]
        domain = tldextract.extract(url).registered_domain
        path = url.replace('https://' + domain, '')
        if domain not in urls_dict:
            urls_dict[domain] = {}
        if path not in urls_dict[domain]:
            urls_dict[domain][path] = []
        urls_dict[domain][path].append(url)

    return urls_dict

# route to display all non-URL comments
@app.route('/comments')
def comments():
    query = "SELECT content FROM messages WHERE content NOT LIKE 'http%'"
    cursor = conn.execute(query)
    messages = [row[0] for row in cursor.fetchall()]
    return render_template('comments.html', messages=messages)

# route to display all URLs sorted by domain and path
@app.route('/urls')
def urls():
    query = "SELECT content FROM messages WHERE content LIKE 'http%'"
    cursor = conn.execute(query)
    urls = [row[0] for row in cursor.fetchall()]
    return render_template('urls.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
