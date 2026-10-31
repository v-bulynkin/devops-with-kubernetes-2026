import os
import requests
from flask import Flask

app = Flask(__name__)

# Path to the shared file in the emptyDir volume
file_path = '/shared/data.txt'
counter_path = '/shared/counter.txt'
config_file_path = '/config/information.txt'

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

    # Get counter via HTTP
    counter_val = "0"
    try:
        response = requests.get('http://ping-pong-svc:5000/pings')
        counter_val = response.text
    except Exception as e:
        counter_val = f"Error: {e}"

    # Get additional config info
    message = os.environ.get('MESSAGE', '')
    file_content = ""
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r') as f:
                file_content = f.read().strip()
        except Exception as e:
            file_content = f"Error reading file: {e}"

    return f"""
    <html>
        <head><title>Log Output</title></head>
        <body>
            <p>file content: {file_content}</p>
            <p>env variable: MESSAGE={message}</p>
            <p>{latest_log_entry}</p>
            <p>Ping / Pongs: {counter_val}</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
