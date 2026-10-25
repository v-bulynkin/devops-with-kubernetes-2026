import time
import uuid
from datetime import datetime, timezone

# Generate GUID
random_id = str(uuid.uuid4())

def log_to_stdout():
    """Generates log entry every 5 sec"""
    file_path = '/shared/data.txt'
    while True:
        # Get current timestamp in ISO 8601 format with UTC 'Z' suffix
        timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
        log_entry = f"{timestamp}: {random_id}"
        print(log_entry)
        
        # Write to the shared file (overwrite mode 'w')
        try:
            with open(file_path, 'w') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error writing to file: {e}")
            
        # Wait for 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    log_to_stdout()
