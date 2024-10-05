from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Directory to save the frames
FRAMES_DIR = "received_frames"

# Ensure the directory exists
if not os.path.exists(FRAMES_DIR):
    os.makedirs(FRAMES_DIR)

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    try:
        # Ensure the request contains a file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        # Get the file from the request
        file = request.files['file']

        # Generate a timestamped filename for the frame
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename = f"frame_{timestamp}.jpg"

        # Save the file to the directory
        file.save(os.path.join(FRAMES_DIR, filename))

        return jsonify({'message': 'Frame received successfully'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the server on all available IP addresses, port 5000
    app.run(host='0.0.0.0', port=5000)