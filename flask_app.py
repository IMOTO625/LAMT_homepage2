from flask import Flask, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'blog_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def start_page():
    with open(DATA_FILE, 'r') as f:
        posts = json.load(f)
    posts.sort(key=lambda x: datetime.fromisoformat(x['timestamp']), reverse=True)
    return render_template('home2.html', posts=posts)

@app.route('/blog')
def blog():
    with open(DATA_FILE, 'r') as f:
        posts = json.load(f)
    posts.sort(key=lambda x: datetime.fromisoformat(x['timestamp']), reverse=True)
    return render_template('blog2.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)