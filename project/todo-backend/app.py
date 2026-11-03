import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
# In production, the app can use a full DATABASE_URL 
# or individual components to support secrets (e.g., DB_PASSWORD from a K8s Secret).
def get_db_uri():
    url = os.environ.get('DATABASE_URL')
    if url:
        # Compatibility with SQLAlchemy 2.0+:
        # if using postgresql://, point to psycopg2 driver explicitly
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', '5432')
    dbname = os.environ.get('DB_NAME', 'todos')

    if user and password:
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    
    return 'sqlite:///todos.db'

app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Get suffix from environment
BACKEND_SUFFIX = os.environ.get('BACKEND_SUFFIX', '/todos')

@app.route(BACKEND_SUFFIX, methods=['GET'])
def get_todos():
    # Return tasks as a list of strings to maintain compatibility with the existing frontend
    todos = Todo.query.all()
    return jsonify([todo.task for todo in todos])

@app.route(BACKEND_SUFFIX, methods=['POST'])
def add_todo():
    data = request.get_json()
    if data and 'todo' in data:
        new_todo = Todo(task=data['todo'])
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    return jsonify({"status": "error"}), 400

# Enable CORS for development purposes
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    if request.method == 'OPTIONS':
        return response, 204
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('BACKEND_PORT', 5000)))
