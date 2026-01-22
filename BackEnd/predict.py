import os
import tensorflow as tf
import numpy as np
import json

IMG_HEIGHT = 64
IMG_WIDTH = 256

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KERAS_PATH = os.path.join(BASE_DIR, "crnn_prescription_model.keras")
H5_PATH = os.path.join(BASE_DIR, "crnn_prescription_model.h5")
MODEL_PATH = KERAS_PATH if os.path.exists(KERAS_PATH) else H5_PATH

model = None
id2word = None


def load_resources():
    global model, id2word
    if model is None:
        print("🔹 Loading CRNN model...")
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Model loaded")

    if id2word is None:
        with open(os.path.join(BASE_DIR, "id2word.json"), "r", encoding="utf-8") as f:
            id2word = json.load(f)
            id2word = {int(k): v for k, v in id2word.items()}


def preprocess_image(image_bytes):
    img = tf.image.decode_png(image_bytes, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
    img = tf.expand_dims(img, axis=0)
    return img


def predict_image_bytes(image_bytes):
    load_resources()

    img = preprocess_image(image_bytes)
    preds = model.predict(img)
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return {
        "prediction": id2word[class_id],
        "confidence": confidence
    }
