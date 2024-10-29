from flask import Flask, jsonify
from datetime import datetime
import threading
import time
import queue

app = Flask(__name__)

# Thread-safe queue to store text that needs to be typed
text_queue = queue.Queue()

# Route to get the next text to type
@app.route('/get_text', methods=['GET'])
def get_text():
    try:
        # Non-blocking get from queue with 1 second timeout
        text = text_queue.get(timeout=1)
        return jsonify({
            'status': 'success',
            'text': text,
            'timestamp': datetime.now().isoformat()
        })
    except queue.Empty:
        return jsonify({
            'status': 'empty',
            'text': '',
            'timestamp': datetime.now().isoformat()
        })

# Route to add new text to the queue
@app.route('/add_text/<text>', methods=['POST'])
def add_text(text):
    text_queue.put(text)
    return jsonify({
        'status': 'success',
        'message': 'Text added to queue',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
