from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
import cv2
import os

app = Flask(__name__)

# Load the trained model
MODEL_NAME = "efficientnet_ingredient_model.h5"
model = tf.keras.models.load_model(MODEL_NAME)

# Load class names
CLASS_NAMES = []
with open("class_names.txt", "r") as f:
    CLASS_NAMES = [line.strip() for line in f.readlines()]

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def predict_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    predicted_class = CLASS_NAMES[np.argmax(prediction)]

    # Save prediction to ing.txt
    with open("ing.txt", "w") as f:
        f.write(predicted_class)

    return predicted_class

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    image_url = None

    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        prediction = predict_image(file_path)
        image_url = file_path

    return render_template("index.html", prediction=prediction, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
