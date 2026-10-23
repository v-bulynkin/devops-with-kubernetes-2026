import os
from flask import Flask

app = Flask(__name__)

# PORT variable
PORT = 5000

@app.route('/')
def index():
    return f"Server started in port {PORT}"

if __name__ == '__main__':
    try:
        PORT = int(os.environ.get("PORT", 5000))
    except ValueError:
        PORT = 5000

    app.run(host='0.0.0.0', port=PORT)
