from flask import Flask, render_template
import sqlite3
import re


app = Flask(__name__)

@app.route("/")
def index():
    # Connect to the database
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    # Fetch all messages from the database
    c.execute("SELECT * FROM messages")
    messages = c.fetchall()

    # Create a list of all URLs mentioned in messages
    urls = []
    for message in messages:
        urls += re.findall(r'(https?://[^\s]+)', message[1])  # URL is in the second column

    # Create a list of all attachments that contain URLs
    attachments = []
    for message in messages:
        if message[2]:  # Check if there is an attachment
            if re.search(r'(https?://[^\s]+)', message[2]):  # Check if there is a URL in the attachment
                attachments.append(message[2])

    # Render the template with the URLs and attachments
    return render_template('index.html', urls=urls, attachments=attachments)

if __name__ == "__main__":
    app.run(debug=True)
