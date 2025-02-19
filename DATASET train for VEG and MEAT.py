import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os
import matplotlib.pyplot as plt

# 📌 Set dataset paths (Update these)
DATASET_PATH = "D:/Balagowdham/dataset"
TRAIN_PATH = os.path.join(DATASET_PATH, "train")
VAL_PATH = os.path.join(DATASET_PATH, "val")
TEST_PATH = os.path.join(DATASET_PATH, "test")  # ✅ Test folder

MODEL_NAME = "efficientnet_ingredient_model.h5"

# 🚀 Step 1: Load and Preprocess Dataset with Augmentation
datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Training Data
train_generator = datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical"
)

# Validation Data
val_generator = datagen.flow_from_directory(
    VAL_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical"
)

# Test Data
test_generator = datagen.flow_from_directory(
    TEST_PATH,
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    shuffle=False
)

# Get number of classes
NUM_CLASSES = len(train_generator.class_indices)
CLASS_NAMES = list(train_generator.class_indices.keys())

# 🔥 Compute Class Weights
labels = train_generator.classes
class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(labels), y=labels)
class_weights_dict = dict(enumerate(class_weights))

# 🚀 Step 2: Build EfficientNetB0 Model
base_model = tf.keras.applications.EfficientNetB0(input_shape=(224, 224, 3), include_top=False, weights="imagenet")
base_model.trainable = False  # Freeze pretrained layers

# Add custom layers
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(NUM_CLASSES, activation="softmax")
])

# Compile Model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

# 🚀 Step 3: Train the Model
early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

history = model.fit(train_generator, 
                    validation_data=val_generator, 
                    epochs=10, 
                    class_weight=class_weights_dict,
                    callbacks=[early_stop])

trained_epochs_1 = len(history.history["loss"])
print(f"✅ Initial Training Completed in {trained_epochs_1} epochs")

# 🚀 Step 4: Fine-Tune the Model
base_model.trainable = True  # Unfreeze layers

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

history_finetune = model.fit(train_generator, 
                             validation_data=val_generator, 
                             epochs=10, 
                             class_weight=class_weights_dict,
                             callbacks=[early_stop])

trained_epochs_2 = len(history_finetune.history["loss"])
total_epochs = trained_epochs_1 + trained_epochs_2
print(f"✅ Fine-Tuning Completed in {trained_epochs_2} epochs")
print(f"✅ Total Training Completed in {total_epochs} epochs")

# 🚀 Step 5: Save the Model
model.save(MODEL_NAME)
print(f"✅ Model saved as {MODEL_NAME}")

# 🚀 Step 6: Evaluate Model
test_loss, test_acc = model.evaluate(test_generator)
print(f"📊 Test Accuracy: {test_acc * 100:.2f}%")

# Save Class Names (Important for Testing)
with open("class_names.txt", "w") as f:
    for class_name in CLASS_NAMES:
        f.write(class_name + "\n")

print("✅ Class names saved!")

# 🚀 Step 7: Plot Accuracy & Loss Graphs
def plot_graphs(history, fine_tune_history):
    plt.figure(figsize=(12, 5))

    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Val Accuracy")
    plt.plot(fine_tune_history.history["accuracy"], label="Fine-tune Train Accuracy", linestyle="dashed")
    plt.plot(fine_tune_history.history["val_accuracy"], label="Fine-tune Val Accuracy", linestyle="dashed")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.title("Training & Validation Accuracy")

    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Val Loss")
    plt.plot(fine_tune_history.history["loss"], label="Fine-tune Train Loss", linestyle="dashed")
    plt.plot(fine_tune_history.history["val_loss"], label="Fine-tune Val Loss", linestyle="dashed")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.title("Training & Validation Loss")

    plt.show()

# Call the function to plot graphs
plot_graphs(history, history_finetune)
