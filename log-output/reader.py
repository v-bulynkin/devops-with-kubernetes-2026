import os
from flask import Flask

app = Flask(__name__)

# Path to the shared file in the emptyDir volume
file_path = '/shared/data.txt'
counter_path = '/shared/counter.txt'

@app.route('/')
def index():
    """HTML page, shows the last generated entry"""
    # Get content from the file
    latest_log_entry = "Initializing..."
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                latest_log_entry = f.read()
        except Exception as e:
            latest_log_entry = f"Error reading file: {e}"

    # Get counter from the file
    counter_val = "0"
    if os.path.exists(counter_path):
        try:
            with open(counter_path, 'r') as f:
                counter_val = f.read()
        except Exception as e:
            counter_val = f"Error reading counter: {e}"

    return f"""
    <html>
        <head><title>Log Output</title></head>
        <body>
            <p>{latest_log_entry}</p>
            <p>Ping / Pongs: {counter_val}</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
