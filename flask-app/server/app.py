# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# Replace the following placeholder function with your actual emotion classification logic
def classify_emotion(photo_data):
    # Placeholder code (replace with your emotion classification model)
    # Assuming you have a function like classify_emotion_model(photo_data)
    # that returns the predicted emotion
    return classify_emotion_model(photo_data)

@app.route('/')
def hello_world():
    return jsonify(message="Nonverb!")

@app.route('/classify_emotion', methods=['POST'])
def classify_emotion_route():
    try:
        data = request.get_json()
        photo_data = data.get('photo')

        # Convert base64 image data to PIL Image
        image = Image.open(io.BytesIO(base64.b64decode(photo_data.split(',')[1])))

        # Perform emotion classification
        emotion = classify_emotion(image)

        return jsonify({'emotion': emotion})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
