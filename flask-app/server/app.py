from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np

app = Flask(__name__)
CORS(app)

# Load pre-trained VGG16 model for image classification
model = VGG16(weights='imagenet')

def classify_emotion_model(image):
    # Resize image to the required input size for VGG16 (224x224)
    image = image.resize((224, 224))

    # Convert PIL Image to NumPy array
    img_array = np.array(image)

    # If the image has an alpha channel, remove it
    if img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]

    # Expand dimensions to match the model input shape (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)

    # Preprocess input according to the requirements of VGG16
    img_array = preprocess_input(img_array)

    # Make prediction
    predictions = model.predict(img_array)

    # Decode predictions
    label = decode_predictions(predictions)[0][0][1]

    return label

@app.route('/classify_emotion', methods=['POST'])
def classify_emotion_route():
    try:
        data = request.get_json()
        photo_data = data.get('photo')

        # Convert base64 image data to PIL Image
        image = Image.open(io.BytesIO(base64.b64decode(photo_data.split(',')[1])))

        # Perform emotion classification
        emotion = classify_emotion_model(image)

        return jsonify({'emotion': emotion})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/')
def hello_world():
    return jsonify(message="Nonverb!")

if __name__ == '__main__':
    app.run(debug=True)
