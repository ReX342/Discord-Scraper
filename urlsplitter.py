from flask import Flask, render_template
import sqlite3
import re

app = Flask(__name__)

@app.route('/')
def index():
    # connect to database
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # query for selecting content field
    query = "SELECT content FROM messages"

    # execute the query and fetch all rows
    c.execute(query)
    rows = c.fetchall()

    # initialize a variable to store URLs
    urls = []

    # iterate over rows and find URLs in content field
    for row in rows:
        content = row[0]
        matches = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', content)
        urls += matches

    # close the database connection
    conn.close()

    # render the index.html template with the urls list
    return render_template('index.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
