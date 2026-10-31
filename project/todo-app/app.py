import os
import random
import time
import requests
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Persistent Volume path
CACHE_DIR = os.environ.get('CACHE_DIR', '/data')
CACHE_FILE_NAME = os.environ.get('CACHE_FILE', 'cached_image.jpg')
CACHE_FILE = os.path.join(CACHE_DIR, CACHE_FILE_NAME)
META_FILE = os.path.join(CACHE_DIR, os.environ.get('META_FILE', 'cache_meta.txt'))
CACHE_DURATION = float(os.environ.get('CACHE_DURATION', 600)) # 10 minutes
IMAGES_BASEURL = os.environ.get('IMAGES_BASEURL', '')
IMAGES_EXTENSION = os.environ.get('IMAGES_EXTENSION', 'jpg')
TEMPLATE_IMAGE_URL = os.environ.get('TEMPLATE_IMAGE_URL', '/static/cached_img.jpg')

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_image_data():
    now = time.time()
    
    # Check if cache file exists and it is not expired
    if os.path.exists(CACHE_FILE) and os.path.exists(META_FILE):
        with open(META_FILE, 'r') as f:
            try:
                timestamp = float(f.read().strip())
            except (ValueError, IOError):
                timestamp = 0
        
        if now - timestamp < CACHE_DURATION:
            return CACHE_FILE

    # If cache expired, download a new picture
    img_number = random.randint(1, 2000)
    url = f"{IMAGES_BASEURL}{img_number}.{IMAGES_EXTENSION}"
    
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

    backend_base_url = os.environ.get('BACKEND_BASE_URL')
    return render_template('index.html', image_url=TEMPLATE_IMAGE_URL, backend_base_url=backend_base_url)

@app.route(TEMPLATE_IMAGE_URL)
def serve_image():
    return send_from_directory(CACHE_DIR, CACHE_FILE_NAME)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('APP_PORT', 5000)))
