import time
import uuid
from datetime import datetime, timezone

def main():
    # Generate GUID
    random_id = str(uuid.uuid4())
    
    try:
        while True:
            # Get current timestamp in ISO 8601 format with UTC 'Z' suffix
            timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")
            print(f"{timestamp}: {random_id}")
            
            # Wait for 5 seconds
            time.sleep(5)
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        pass

if __name__ == "__main__":
    main()
