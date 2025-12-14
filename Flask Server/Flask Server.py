from flask import Flask, request, send_file, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'C:\\Users\\zhaoy\\Desktop\\IoT\\Flask Server\\Uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Option 1: Keep only latest image
        filepath = os.path.join(UPLOAD_FOLDER, 'latest.jpg')
        
        # Option 2: Save with timestamp (uncomment if you want to keep history)
        # timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # filepath = os.path.join(UPLOAD_FOLDER, f'image_{timestamp}.jpg')
        
        with open(filepath, 'wb') as f:
            f.write(request.data)
        
        print(f"Image saved at {datetime.now()}")
        return 'OK', 200
    except Exception as e:
        print(f"Error: {e}")
        return 'Error', 500

@app.route('/image')
def get_image():
    filepath = os.path.join(UPLOAD_FOLDER, 'latest.jpg')
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg')
    return 'No image available', 404

@app.route('/')
def index():
    # Simple HTML page that auto-refreshes the image
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Camera Feed</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f0f0;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            #camera-feed {
                max-width: 800px;
                width: 100%;
                border: 3px solid #333;
                border-radius: 10px;
                margin: 20px auto;
                display: block;
            }
            .info {
                color: #666;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <h1>ESP32 Camera Live Feed</h1>
        <p class="info">Auto-refreshing every 5 seconds</p>
        <img id="camera-feed" src="/image" alt="Camera Feed">
        
        <script>
            // Refresh image every 5 seconds
            setInterval(function() {
                document.getElementById('camera-feed').src = '/image?' + new Date().getTime();
            }, 5000);
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    print("Starting ESP32 Camera Server...")
    print("View the camera feed at: http://192.168.0.2:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)