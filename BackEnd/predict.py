import tensorflow as tf
import numpy as np
import json

IMG_HEIGHT = 64
IMG_WIDTH  = 256

# ✅ Load trained model
model = tf.keras.models.load_model("crnn_prescription_model.keras")

# ✅ Load label decoder
with open("id2word.json", "r") as f:
    id2word = json.load(f)
    id2word = {int(k): v for k, v in id2word.items()}

def preprocess_image(image_bytes):
    img = tf.image.decode_png(image_bytes, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
    img = tf.expand_dims(img, axis=0)  # (1, 64, 256, 1)
    return img

def predict_image_bytes(image_bytes):
    img = preprocess_image(image_bytes)
    preds = model.predict(img)
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return {
        "prediction": id2word[class_id],
        "confidence": confidence
    }
