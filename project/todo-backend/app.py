from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for todos
todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if data and 'todo' in data:
        todos.append(data['todo'])
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "error"}), 400

# Enable CORS for development purposes
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    if response.method == 'OPTIONS':
        return response, 204
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
