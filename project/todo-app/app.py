import os
import random
import time
import requests
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Persistent Volume path
CACHE_DIR = os.environ.get('CACHE_DIR')
CACHE_FILE = os.path.join(CACHE_DIR, os.environ.get('CACHE_FILE'))
META_FILE = os.path.join(CACHE_DIR, os.environ.get('META_FILE'))
CACHE_DURATION = os.environ.get('CACHE_DURATION') # 10 minutes

def get_image_data():
    now = time.time()
    
    # Check if cache file exists and it is not expired
    if os.path.exists(CACHE_FILE) and os.path.exists(META_FILE):
        with open(META_FILE, 'r') as f:
            timestamp = float(f.read().strip())
        
        if now - timestamp < CACHE_DURATION:
            return CACHE_FILE

    # If cache expired, download a new picture
    # https://picsum.photos/1200 is unavailable, using another resource
    img_number = random.randint(1, 2000)
    url = f"{os.environ.get('IMAGES_BASEURL')}{img_number}.{os.environ.get('IMAGES_EXTENSION')}"
    
    print(f"Downloading new image: {url}")
    
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Save image to PV
            with open(CACHE_FILE, 'wb') as f:
                f.write(response.content)
            
            # Save download time
            with open(META_FILE, 'w') as f:
                f.write(str(now))
                
            return CACHE_FILE
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(1)
            else:
                print("All retry attempts failed.")
    
    return None

@app.route('/')
def index():
    image_path = get_image_data()
    if not image_path:
        return "Error loading image", 500

    # API_BASE_URL (backend external address like http://k1:8081) must be set in deployment env
    backend_base_url = os.environ.get('BACKEND_BASE_URL')
    template_image_url = os.environ.get('TEMPLATE_IMAGE_URL')

    # Return image path (through serve_from_directory)
    return render_template('index.html', image_url=template_image_url, backend_base_url=backend_base_url)

@app.route(template_image_url)
def serve_image():
    return send_from_directory(CACHE_DIR, os.environ.get('CACHE_FILE'))

if __name__ == '__main__':
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    app.run(host='0.0.0.0', port=os.environ.get('APP_PORT'))
