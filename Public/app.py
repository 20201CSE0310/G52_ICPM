from flask import Flask, request, jsonify, render_template
from PIL import Image
from flask_cors import CORS, cross_origin
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import os

app = Flask(__name__)
CORS(app)

model = load_model('plant_disease_model.h5')


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224)) 
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  
    return img_array


def make_prediction(img_path):
    img_array = preprocess_image(img_path)
    prediction = model.predict(img_array)
    return prediction.tolist()



@app.route('/')
def index():
    return render_template('disease-prediction.html')

@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        upload_path = 'temp_image.jpg'
        file.save(upload_path)


        prediction = make_prediction(upload_path)


        os.remove(upload_path)

        return jsonify({'prediction': prediction})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)