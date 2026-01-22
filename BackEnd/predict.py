import os
import tensorflow as tf
import numpy as np
import json

IMG_HEIGHT = 64
IMG_WIDTH = 256

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = (
    os.path.join(BASE_DIR, "crnn_prescription_model.keras")
    if os.path.exists(os.path.join(BASE_DIR, "crnn_prescription_model.keras"))
    else os.path.join(BASE_DIR, "crnn_prescription_model.h5")
)

model = None
id2word = None

def load_resources():
    global model, id2word

    if model is None:
        model = tf.keras.models.load_model(MODEL_PATH)

    if id2word is None:
        with open(os.path.join(BASE_DIR, "id2word.json"), "r") as f:
            id2word = {int(k): v for k, v in json.load(f).items()}

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
    return {
        "prediction": id2word[int(np.argmax(preds))],
        "confidence": float(np.max(preds))
    }
