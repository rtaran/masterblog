from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Path to the data directory
DATA_DIR = 'data'
POSTS_FILE = os.path.join(DATA_DIR, 'posts.json')

def load_posts():
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # Create empty posts file if it doesn't exist
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'w') as f:
            json.dump([], f)

    with open(POSTS_FILE, 'r') as f:
        return json.load(f)


def save_posts(posts):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing posts and generate new ID
        posts = load_posts()
        new_id = max(post['id'] for post in posts) + 1 if posts else 1

        # Create new post and save
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')

# ... rest of your existing routes ...