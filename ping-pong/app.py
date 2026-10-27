import os
from flask import Flask

app = Flask(__name__)

counter = 0

@app.route('/pingpong', methods=['GET'])
def ping_pong():
    global counter
    counter += 1
    return f"pong {counter}"

@app.route('/pings')
def pings():
    """Returns the current counter value"""
    return str(counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
