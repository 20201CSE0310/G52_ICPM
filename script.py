import sys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

def load_custom_model(model_path):
    try:
        model = load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

def preprocess_image(image_path, target_size=(224, 224)):
    try:
        img = image.load_img(image_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.
        return img_array
    except Exception as e:
        print(f"Error preprocessing the image: {e}")
        return None

def make_predictions(model, img_array, class_labels):
    try:
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = class_labels[predicted_class_index]
        return predicted_class_label
    except Exception as e:
        print(f"Error making predictions: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 script.py image_path model_path")
        return

    image_path = sys.argv[1]
    model_path = sys.argv[2]

    model = load_custom_model(model_path)

    if model is not None:
        img_array = preprocess_image(image_path)

        if img_array is not None:
            class_labels = ['Pepper_bell__Bacterial_spot',
'Potato___Late_blight',
'Tomato_healthy',
'Tomato_Leaf_Mold',
'Pepper_bell__healthy',
'Tomato_Septoria_leaf_spot',
'Tomato_Spider_mites_Two_spotted_spider_mite',
'Tomato_Early_blight',
'Tomato_Late_blight',
'Tomato__Tomato_mosaic_virus',
'Potato___Early_blight',
'Tomato_Tomato_YellowLeaf_Curl_Virus',
'Potato___healthy',
'Tomato__Target_Spot',
'Tomato_Bacterial_spot']  
            prediction = make_predictions(model, img_array, class_labels)

            if prediction is not None:
                print("Predicted Class Label:", prediction.title().replace("_", ""))

                
            else:
                print("Failed to make predictions.")
        else:
            print("Failed to load and preprocess the image.")
    else:
        print("Failed to load the model.")

if __name__ == "__main__":
    main()
