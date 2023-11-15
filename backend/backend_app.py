from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_title(new_post):
    if "title" not in new_post:
        return False
    return True


def validate_content(new_post):
    if "content" not in new_post:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_title(new_post):
            return jsonify({"error": "Missing post title"}), 400
        if not validate_content(new_post):
            return jsonify({"error": "Missing post content"}), 400
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post)

    return jsonify(POSTS)


def delete_post(id):
    for post in POSTS:
        if post['id'] == id:
            deleted_post = post
            POSTS.remove(post)
            return deleted_post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def del_post(id):
    post = delete_post(id)
    if post is None:
        return '', 404
    return jsonify(post)


def update_title(id, updated_post):
    for post in POSTS:
        if post['id'] == id:
            post['title'] = updated_post['title']
            return post
    return None


def update_content(id, updated_post):
    for post in POSTS:
        if post['id'] == id:
            post['content'] = updated_post['content']
            return post
    return None


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
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    results = []
    if title_query:
        for post in POSTS:
            if title_query.lower() in post['title'].lower():
                results.append(post)
    if content_query:
        for post in POSTS:
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
