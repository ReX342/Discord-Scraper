import requests
import json
import sqlite3
from tqdm import tqdm

def create_table():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages
        (id TEXT PRIMARY KEY,
         author TEXT,
         content TEXT,
         timestamp TEXT)
    ''')
    conn.commit()
    conn.close()

def retrieve_messages(channelid):
    headers = {
        'authorization': 'https://youtu.be/xh28F6f-Cds'
    }
    messages = []
    before = None
    total_messages = 0
    with tqdm(total=1000, desc='Retrieving messages') as pbar1:
        while True:
            url = f'https://discord.com/api/v9/channels/{channelid}/messages'
            if before:
                url += f'?before={before}'
            r = requests.get(url, headers=headers)
            jsonn = json.loads(r.text)
            if not jsonn:
                break
            messages += jsonn
            before = jsonn[-1]['id']
            total_messages += len(jsonn)
            if total_messages % 1000 == 0:
                pbar1.update(1000)
                with tqdm(total=total_messages, desc='Inserting into database') as pbar2:
                    conn = sqlite3.connect('messages.db')
                    c = conn.cursor()
                    for value in messages:
                        id = value['id']
                        author = value['author']['username']
                        content = value['content']
                        timestamp = value['timestamp']
                        c.execute('INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?)', (id, author, content, timestamp))
                        pbar2.update(1)
                    conn.commit()
                    conn.close()
                    messages = []
            else:
                pbar1.update(len(jsonn))
            
    if messages:
        with tqdm(total=total_messages % 1000, desc='Inserting remaining messages') as pbar2:
            conn = sqlite3.connect('messages.db')
            c = conn.cursor()
            for value in messages:
                id = value['id']
                author = value['author']['username']
                content = value['content']
                timestamp = value['timestamp']
                c.execute('INSERT OR IGNORE INTO messages VALUES (?, ?, ?, ?)', (id, author, content, timestamp))
                pbar2.update(1)
            conn.commit()
            conn.close()
    
create_table()
retrieve_messages('1011735697486512219')