from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_posts():
    """Load blog posts from JSON file"""
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as f:
            return json.load(f)
    else:
        # Initial data if file doesn't exist
        initial_posts = [
            {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
            {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
        ]
        with open('/data/posts.json', 'w') as f:
            json.dump(initial_posts, f, indent=4)
        return initial_posts


def save_posts(posts):
    """Save blog posts to JSON file"""
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=4)


def generate_new_id(posts):
    """Generate a new unique ID for a blog post"""
    if not posts:
        return 1
    return max(post['id'] for post in posts) + 1


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing posts
        posts = load_posts()

        # Generate new ID
        new_id = generate_new_id(posts)

        # Create new post
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Add new post to list
        posts.append(new_post)

        # Save updated posts
        save_posts(posts)

        # Redirect to home page
        return redirect(url_for('index'))

    # If GET request, display form
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)