from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def load_posts():
    try:
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)
        return blog_posts
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. Returning an empty list.")
        return []


def save_posts(posts):
    try:
        with open('blog_posts.json', 'w') as file:
            json.dump(posts, file, indent=4)
    except Exception as e:
        print(f"Error saving posts: {e}")


def validate_title(new_post):
    if "title" not in new_post:
        return False
    return True


def validate_content(new_post):
    if "content" not in new_post:
        return False
    return True


def sort_posts_content(posts, direction):
    if direction == "asc":
        sorted_posts = sorted(posts, key=lambda x: x['content'])
        return sorted_posts
    if direction == "desc":
        sorted_posts = sorted(posts, key=lambda x: x['content'], reverse=True)
        return sorted_posts
    return None


def sort_posts_title(posts, direction):
    if direction == "asc":
        sorted_posts = sorted(posts, key=lambda x: x['title'])
        return sorted_posts
    if direction == "desc":
        sorted_posts = sorted(posts, key=lambda x: x['title'], reverse=True)
        return sorted_posts
    return None


def update_title(id, updated_post):
    posts = load_posts()
    for post in posts:
        if post['id'] == id:
            post['title'] = updated_post['title']
            save_posts(posts)
            return post
    return None


def update_content(id, updated_post):
    posts = load_posts()
    for post in posts:
        if post['id'] == id:
            post['content'] = updated_post['content']
            save_posts(posts)
            return post
    return None


def delete_post(id):
    posts = load_posts()
    for post in posts:
        if post['id'] == id:
            deleted_post = post
            posts.remove(post)
            save_posts(posts)
            return deleted_post
    return None


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    posts = load_posts()
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_title(new_post):
            return jsonify({"error": "Missing post title"}), 400
        if not validate_content(new_post):
            return jsonify({"error": "Missing post content"}), 400
        new_id = max(post['id'] for post in posts) + 1
        new_post['id'] = new_id
        posts.append(new_post)
        return jsonify(new_post)

    sort_query = request.args.get('sort')
    direction = request.args.get('direction')
    if direction and sort_query:
        if sort_query == "title":
            sorted_posts = sort_posts_title(posts, direction)
            if sorted_posts:
                return jsonify(sorted_posts)
            return jsonify({"error": "Invalid direction"}), 400
        if sort_query == "content":
            sorted_posts = sort_posts_content(posts, direction)
            if sorted_posts:
                return jsonify(sorted_posts)
            return jsonify({"error": "Invalid direction"}), 400
        return jsonify({"error": "Invalid sorting field"}), 400

    return jsonify(posts)


@app.route('/api/posts/add', methods=['POST'])
def add():
    posts = load_posts()
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('content')
    new_id = max(post['id'] for post in posts) + 1 if posts else 1
    new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}
    posts.append(new_post)
    save_posts(posts)
    return jsonify(new_post)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def del_post(id):
    post = delete_post(id)
    if post is None:
        return '', 404
    return jsonify(post)


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    updated_post = request.get_json()
    if validate_title(updated_post):
        post = update_title(id, updated_post)
        if post is not None:
            return jsonify(post)
        return '', 404
    if validate_content(updated_post):
        post = update_content(id, updated_post)
        if post is not None:
            return jsonify(post)
        return '', 404


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    posts = load_posts()
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    results = []
    if title_query:
        for post in posts:
            if title_query.lower() in post['title'].lower():
                results.append(post)
    if content_query:
        for post in posts:
            if content_query.lower() in post['content'].lower():
                results.append(post)
    if results:
        return jsonify(results)
    return '', 404


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
