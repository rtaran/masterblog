from flask import Flask, render_template, request, redirect, url_for, abort
import json
import os

app = Flask(__name__)

# File paths
DATA_DIR = 'data'
POSTS_FILE = os.path.join(DATA_DIR, 'posts.json')


def load_posts():
    """Load posts from JSON file with backward compatibility."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'w') as f:
            json.dump([], f)

    with open(POSTS_FILE, 'r') as f:
        posts = json.load(f)

    # Ensure all posts have 'likes' field
    for post in posts:
        if 'likes' not in post:
            post['likes'] = 0
    return posts


def save_posts(posts):
    """Save posts to JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    """Display all blog posts."""
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        posts = load_posts()
        new_id = max(post['id'] for post in posts) + 1 if posts else 1

        new_post = {
            'id': new_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content'],
            'likes': 0
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete a blog post."""
    posts = load_posts()
    updated_posts = [post for post in posts if post['id'] != post_id]
    save_posts(updated_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post."""
    posts = load_posts()
    post_index = next((i for i, p in enumerate(posts) if p['id'] == post_id), None)

    if post_index is None:
        abort(404)

    if request.method == 'POST':
        posts[post_index] = {
            'id': post_id,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content'],
            'likes': posts[post_index]['likes']  # Preserve likes
        }
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=posts[post_index])


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    """Increment like count for a post."""
    posts = load_posts()
    post_index = next((i for i, p in enumerate(posts) if p['id'] == post_id), None)

    if post_index is None:
        abort(404)

    posts[post_index]['likes'] += 1
    save_posts(posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)