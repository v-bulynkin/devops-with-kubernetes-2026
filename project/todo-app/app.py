import os
import random
import time
import requests
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Persistent Volume path
CACHE_DIR = '/data'
CACHE_FILE = os.path.join(CACHE_DIR, 'cached_image.jpg')
META_FILE = os.path.join(CACHE_DIR, 'cache_meta.txt')
CACHE_DURATION = 600  # 10 minutes

def get_image_data():
    now = time.time()
    
    # Check if cache file exists and it is not expired
    if os.path.exists(CACHE_FILE) and os.path.exists(META_FILE):
        with open(META_FILE, 'r') as f:
            timestamp = float(f.read().strip())
        
        if now - timestamp < CACHE_DURATION:
            return CACHE_FILE

    # Если кэш протух или его нет, скачиваем новый
    img_number = random.randint(1, 2000)
    url = f"https://yavuzceliker.github.io/sample-images/image-{img_number}.jpg"
    
    print(f"Downloading new image: {url}")
    
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
        print(f"Error downloading image: {e}")
        return None

@app.route('/')
def index():
    image_path = get_image_data()
    if not image_path:
        return "Error loading image", 500
    
    # Return image path (through serve_from_directory)
    return render_template('index.html', image_url='/static/cached_img.jpg')

@app.route('/static/cached_img.jpg')
def serve_image():
    return send_from_directory(CACHE_DIR, 'cached_image.jpg')

if __name__ == '__main__':
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    app.run(host='0.0.0.0', port=5000)
