import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models

# ============================================================
# STEP 1 — PATHS
# ============================================================

BASE = r"C:\Doctor’s Handwritten Prescription BD dataset"

TRAIN_CSV = BASE + r"\Training\training_labels.csv"
TRAIN_IMG = BASE + r"\Training\training_words"

VAL_CSV   = BASE + r"\Validation\validation_labels.csv"
VAL_IMG   = BASE + r"\Validation\validation_words"

TEST_CSV  = BASE + r"\Testing\testing_labels.csv"
TEST_IMG  = BASE + r"\Testing\testing_words"

# ============================================================
# STEP 2 — IMAGE / TRAINING PARAMS
# ============================================================

IMG_HEIGHT = 64
IMG_WIDTH  = 256
BATCH_SIZE = 32
AUTOTUNE   = tf.data.AUTOTUNE

# ============================================================
# STEP 3 — CLEAN MEDICINE WORDS
# ============================================================

def clean_word(word):
    word = word.replace(" ", "")
    word = word.replace("-", "")
    return word.strip()

# ============================================================
# STEP 4 — BUILD WORD VOCABULARY
# ============================================================

def load_all_labels():
    train_df = pd.read_csv(TRAIN_CSV)
    val_df   = pd.read_csv(VAL_CSV)
    test_df  = pd.read_csv(TEST_CSV)

    all_words = pd.concat([train_df, val_df, test_df], ignore_index=True)
    all_words["MEDICINE_NAME"] = all_words["MEDICINE_NAME"].apply(clean_word)

    unique_words = sorted(all_words["MEDICINE_NAME"].unique())

    word2id = {w:i for i, w in enumerate(unique_words)}
    id2word = {i:w for w, i in word2id.items()}

    print("Total unique:", len(unique_words))
    return word2id, id2word

word2id, id2word = load_all_labels()
NUM_CLASSES = len(word2id)

# ============================================================
# STEP 5 — DATASET PIPELINE (NO AUGMENTATION)
# ============================================================

def load_dataframe(csv_path):
    df = pd.read_csv(csv_path)
    df["MEDICINE_NAME"] = df["MEDICINE_NAME"].apply(clean_word)
    return df

def make_dataset(csv_path, img_dir, shuffle=False):
    df = load_dataframe(csv_path)

    img_paths = [
        os.path.join(img_dir, str(f).strip())
        for f in df["IMAGE"]
    ]

    labels = [word2id[w] for w in df["MEDICINE_NAME"]]

    img_paths = np.array(img_paths)
    labels    = np.array(labels, dtype=np.int32)

    ds = tf.data.Dataset.from_tensor_slices((img_paths, labels))

    def _load_fn(path, label):
        img_bytes = tf.io.read_file(path)
        img = tf.image.decode_png(img_bytes, channels=1)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])
        return img, label

    ds = ds.map(_load_fn, num_parallel_calls=AUTOTUNE)

    if shuffle:
        ds = ds.shuffle(len(labels), reshuffle_each_iteration=True)

    return ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)

train_ds = make_dataset(TRAIN_CSV, TRAIN_IMG, shuffle=True)
val_ds   = make_dataset(VAL_CSV,   VAL_IMG)
test_ds  = make_dataset(TEST_CSV,  TEST_IMG)

# ============================================================
# STEP 6 — ORIGINAL CRNN (NO BATCHNORM, NO AUGMENTATION)
# ============================================================

def build_crnn():
    inputs = layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))

    x = layers.Conv2D(32, 3, padding="same", activation="relu")(inputs)
    x = layers.MaxPooling2D((2,2))(x)

    x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = layers.MaxPooling2D((2,2))(x)

    x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = layers.MaxPooling2D((2,2))(x)

    x = layers.Permute((2, 1, 3))(x)
    x = layers.Reshape((IMG_WIDTH // 8, (IMG_HEIGHT // 8) * 128))(x)

    x = layers.Bidirectional(layers.LSTM(128))(x)

    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)

    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    return models.Model(inputs, outputs)

model = build_crnn()
model.summary()

# ============================================================
# STEP 7 — COMPILE (STABLE LR)
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

# ============================================================
# STEP 8 — CALLBACKS
# ============================================================

checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    "best_crnn.keras",
    monitor="val_accuracy",
    mode="max",
    save_best_only=True,
    verbose=1,
)

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=6,
    restore_best_weights=True,
    verbose=1,
)

# ============================================================
# STEP 9 — TRAIN (NO LR DECAY)
# ============================================================

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=40,
    callbacks=[early_stop, checkpoint_cb],
)

# ============================================================
# STEP 10 — EVALUATE
# ============================================================

loss, acc = model.evaluate(test_ds)
print(f"\n[CRNN LAST MODEL] Test accuracy: {acc:.4f}")

best_model = tf.keras.models.load_model("best_crnn.keras")
loss, acc = best_model.evaluate(test_ds)
print(f"[BEST CRNN MODEL] Test accuracy: {acc:.4f}")

# ============================================================
# STEP 11 — SAMPLE PREDICTIONS
# ============================================================

print("\n--- SAMPLE CRNN PREDICTIONS ---")

for images, labels in test_ds.take(1):
    preds = best_model.predict(images)
    ids = np.argmax(preds, axis=1)

    for i in range(len(ids)):
        print(f"\nImage #{i}")
        print("True label:     ", id2word[int(labels[i])])
        print("CRNN predicted:", id2word[int(ids[i])])
