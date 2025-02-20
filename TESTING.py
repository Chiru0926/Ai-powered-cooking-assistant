import tensorflow as tf
import numpy as np
import cv2
import os

# 📌 Load trained model
MODEL_NAME = "efficientnet_ingredient_model.h5"
model = tf.keras.models.load_model(MODEL_NAME)

# 📌 Class labels (Ensure these match your training classes)
CLASS_NAMES = ['class1', 'class2', 'class3']  # 🔴 Update with actual class names

# 🚀 Function to preprocess test image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"⚠️ Error: Could not load image {image_path}")
        return None

    h, w, _ = img.shape  # Get original dimensions

    # 🔹 Center crop to make square
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    img_cropped = img[start_y:start_y + min_dim, start_x:start_x + min_dim]

    # 🔹 Resize to 224x224
    img_resized = cv2.resize(img_cropped, (224, 224))
    img_normalized = img_resized / 255.0  # Normalize pixel values
    img_final = np.expand_dims(img_normalized, axis=0)  # Add batch dimension

    return img_final

# 🚀 Function to predict class from image
def predict_image(image_path):
    processed_img = preprocess_image(image_path)  # Apply preprocessing
    if processed_img is None:
        return "⚠️ Invalid image!"

    prediction = model.predict(processed_img)
    predicted_class = np.argmax(prediction)  # Get class index
    confidence = np.max(prediction)  # Get confidence score
    
    return CLASS_NAMES[predicted_class], confidence

# 📌 Test with an image
TEST_IMAGE = "test_image.jpg"  # 🔴 Replace with actual test image path
if os.path.exists(TEST_IMAGE):
    predicted_label, confidence = predict_image(TEST_IMAGE)
    print(f"🔍 Predicted Class: {predicted_label} (Confidence: {confidence:.2f})")
else:
    print("⚠️ Test image not found! Please provide a test image.")
