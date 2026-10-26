import os
from flask import Flask

app = Flask(__name__)

counter = 0

@app.route('/pingpong', methods=['GET'])
def ping_pong():
    global counter
    counter += 1
    try:
        with open('/shared/counter.txt', 'w') as f:
            f.write(str(counter))
    except Exception as e:
        print(f"Error writing counter: {e}")
    return f"pong {counter}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
