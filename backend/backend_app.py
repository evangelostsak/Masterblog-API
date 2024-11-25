from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

id_stat = len(POSTS) + 1


def new_id_gen():
    """Generates a unique id using our global id counter 'id_stat' """
    global id_stat
    new_id = id_stat
    id_stat += 1
    return new_id


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Post listing"""
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add Endpoint"""
    data = request.get_json()

    # Error handling part for title and content + strip for cleanup
    if not data:
        return jsonify({"error": "Request must be json"}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title:
        return jsonify({"error": "Title is a required field"}), 400
    if not content:
        return jsonify({"error": "Content is a required field"}), 400

    # ID generation process
    new_post = {
        "id": new_id_gen(),
        "title": title,
        "content": content
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete endpoint for posts, ID based"""
    for post in POSTS:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {post_id} has been successfully deleted."}), 200
    # Error handling if wrong post id 404
    return jsonify({"error": f"Post with {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Updates an existing post (title, content)"""
    data = request.get_json()

    for post in POSTS:
        post['title'] = data.get('title', post['title']).strip()
        post['content'] = data.get('content', post['content']).strip()

        return jsonify(post), 200
    # Error handling 404
    return jsonify({"error": f"Post with id {post_id} not found."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
