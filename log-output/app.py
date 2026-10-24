import time
import uuid
import threading
from datetime import datetime, timezone
from flask import Flask

# Generate GUID
random_id = str(uuid.uuid4())

# Global env for keeping last log string
latest_log_entry = "Initializing..."

def log_to_stdout():
    """Generates log entry every 5 sec"""
    global latest_log_entry
    while True:
        # Get current timestamp in ISO 8601 format with UTC 'Z' suffix
        timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
        log_entry = f"{timestamp}: {random_id}"
        print(log_entry)
        latest_log_entry = log_entry
        # Wait for 5 seconds
        time.sleep(5)

app = Flask(__name__)

@app.route('/')
def index():
    """HTML page, shows the last generated entry"""
    return f"""
    <html>
        <head><title>Log Output</title></head>
        <body>
            <p>{latest_log_entry}</p>
        </body>
    </html>
    """

# Start background thread for logs generation
threading.Thread(target=log_to_stdout, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)