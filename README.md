## Doctor Handwritten Prescription AI

Doctor Handwritten Prescription AI is a full-stack application that classifies a handwritten prescription image as a medicine name and displays the model confidence. When matching medicine data is available, the frontend also shows the corresponding safety information.

This is an educational portfolio project for exploring image classification, TensorFlow model serving, and frontend-to-backend integration. It is not a diagnostic or prescribing tool.

## The Problem

Handwritten medicine names are difficult to interpret consistently, especially when the source image is noisy or the handwriting is unclear. This project explores a constrained version of that problem: recognizing medicine-word classes from prescription images using a trained neural network.

## Why I Built It

The repository combines a trained image model with a usable browser workflow. It demonstrates how to:

- accept an uploaded image in a React interface
- send the image to a Python API as multipart form data
- preprocess the image for a TensorFlow model
- map the predicted class to a medicine name
- look up local medicine safety information
- present prediction confidence and results in the UI

## Key Features

- Upload a prescription image and preview it in the browser.
- Submit the image to the backend prediction endpoint.
- Convert the model output into a medicine name and confidence percentage.
- Look up medicine information from the bundled `medicine_data.json` file.
- Resolve a known brand name to its generic medicine when the data file contains that mapping.
- Display medicine safety fields in a modal dialog.
- Show connection and missing-medicine errors in the frontend.

## System Architecture

```text
React + Vite frontend
    |
    | POST /predict (multipart image)
    v
FastAPI application
    |
    v
TensorFlow/Keras model
    |
    | predicted class + softmax confidence
    v
React result view
    |
    | GET /medicine/{name}
    v
Bundled medicine_data.json
    |
    v
Safety information modal
```

The frontend currently calls the deployed backend URL hard-coded in `frontend/src/component/mainpage.jsx`:
`https://doctor-handwritten-prescription-ai.onrender.com`.

## Tech Stack

### Programming Languages

- Python
- JavaScript
- HTML and CSS

### Frontend

- React 19
- React DOM
- Vite
- ESLint

### Backend

- FastAPI
- Uvicorn
- `python-multipart` for uploaded files
- FastAPI CORS middleware

### AI / Machine Learning / Computer Vision

- TensorFlow and Keras
- NumPy
- Pandas for the training-data pipeline in `BackEnd/Project.py`
- A bundled `.keras` model, with an `.h5` fallback
- Grayscale image decoding, normalization, and resizing with `tf.image`
- A CRNN-style training script in `BackEnd/Project.py` using convolutional layers, a bidirectional LSTM, and a softmax classifier

`opencv-python` and `Pillow` are listed in the backend requirements, but the inspected Python source does not directly import either library. No standalone Tesseract, EasyOCR, or other OCR package is used.

### Data and Storage

- JSON files for the medicine data and model vocabulary
- No database is configured or used

### Cloud / External Services

- The frontend is configured to call a Render-hosted backend at `https://doctor-handwritten-prescription-ai.onrender.com`.
- No external AI API or third-party medicine service is used by the application code.

### Development Tools

- npm and the committed `frontend/package-lock.json`
- Uvicorn development server
- ESLint

## How It Works

1. The user selects an image in the React frontend.
2. The browser creates a local preview with `FileReader`.
3. Clicking **Run Prediction** sends the file as the `file` field in a `POST /predict` request.
4. The backend decodes the bytes as PNG, converts the image to one grayscale channel, normalizes it, and resizes it to `64 x 256` pixels.
5. The backend lazily loads `crnn_prescription_model.keras` when available, otherwise it uses `crnn_prescription_model.h5`.
6. The highest-probability class is mapped through `id2word.json` and returned as `prediction` with a numeric `confidence`.
7. The frontend requests `GET /medicine/{prediction}` and, when a match exists, renders the returned safety fields in a modal.

The backend also exposes `GET /`, which returns a simple status response.

## API Surface

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/` | Returns a backend status response |
| `POST` | `/predict` | Accepts an uploaded image in the `file` form field and returns a prediction and confidence |
| `GET` | `/medicine/{name}` | Returns generic/brand information and safety data when the medicine exists in the bundled JSON |

## Technical Challenges

- **Image input constraints:** The inference path uses TensorFlow PNG decoding and a fixed `64 x 256` input shape, so input format and normalization affect whether prediction succeeds.
- **Class vocabulary management:** Predictions are integer class IDs and require the bundled `id2word.json` mapping to produce medicine names.
- **Model and API integration:** The backend must load large model resources and return a small JSON response suitable for the browser.
- **Medicine matching:** The lookup endpoint handles exact generic names, brand-to-generic mappings, and case-insensitive generic-name fallback.
- **Medical safety communication:** The UI labels the system as educational and warns users not to use its output for diagnosis or treatment.

## Project Structure

```text
doctor-handwritten-prescription-ai/
├── BackEnd/
│   ├── main.py                         # FastAPI routes
│   ├── predict.py                      # Model loading and inference
│   ├── Project.py                      # CRNN training/evaluation script
│   ├── crnn_prescription_model.keras   # Preferred inference model
│   ├── crnn_prescription_model.h5      # Fallback inference model
│   ├── id2word.json                    # Class ID to medicine mapping
│   ├── medicine_data.json              # Medicine safety data and mappings
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── component/mainpage.jsx      # Upload, prediction, and result UI
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
└── README.md
```

## Installation

### Prerequisites

- Python with TensorFlow support
- Node.js and npm
- The model and JSON files included in `BackEnd/`

### Backend

From the repository root:

```bash
cd BackEnd
python -m venv .venv
```

Activate the environment, then install the declared runtime dependencies:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**macOS/Linux**

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the API from inside `BackEnd/`:

```bash
uvicorn main:app --reload
```

The local API will normally be available at `http://127.0.0.1:8000`.

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite server will print the local frontend URL, normally `http://localhost:5173`.

## Usage

1. Start the backend and frontend using the commands above.
2. Open the Vite URL in a browser.
3. Select a prescription image.
4. Review the image preview and click **Run Prediction**.
5. Review the predicted medicine and confidence.
6. If the medicine exists in the bundled data, review its safety information.

The frontend does not currently read an environment variable for the API URL. For local backend testing, change `API_BASE` in `frontend/src/component/mainpage.jsx` from the Render URL to `http://127.0.0.1:8000`.

## Screenshots

The repository contains a logo asset but no application screenshots.

<!-- Add application screenshots here -->

## Results / Evaluation

The repository contains training and test-evaluation code in `BackEnd/Project.py`, including accuracy output for the test set and a best-checkpoint evaluation. However, no recorded accuracy, dataset size, inference-time measurement, or other benchmark result is included in the repository. No performance numbers are claimed here.

## Limitations

- The inference code decodes PNG bytes specifically; other image formats may not work even though the browser file input is generic.
- The model returns one medicine class rather than a structured prescription containing dosage, frequency, duration, or multiple medicines.
- Confidence is the maximum softmax probability and is not presented as a calibrated medical certainty.
- The frontend depends on a hard-coded backend URL and has no environment-based configuration.
- The training script uses a developer-specific Windows dataset path (`C:\Doctor's Handwritten Prescription BD dataset`) and is not directly reproducible without that dataset and its expected CSV/image layout.
- The training script imports Pandas, but `BackEnd/requirements.txt` does not currently include it; the listed requirements are sufficient only for the checked-in inference API after the other dependencies are installed.
- The backend enables permissive CORS for all origins.
- There are no automated application tests in the repository.

## Future Improvements

- Add environment-based frontend API configuration.
- Validate file types and return clearer backend errors for unsupported images.
- Add automated backend and frontend tests.
- Publish reproducible dataset and training instructions without machine-specific paths.
- Record and publish evaluation metrics from a defined held-out test set.
- Add calibrated confidence or abstention behavior for uncertain predictions.
- Support structured extraction of medicine, dosage, frequency, and duration.
- Restrict CORS and add production-oriented request validation.

## Medical Disclaimer

> **This project is for educational, research, and portfolio purposes only.**
>
> It is not a certified medical device. Do not use its output to identify medication, determine dosage, change treatment, or make medical decisions. Prescription information must be verified by a qualified healthcare professional.

## Author

**Murhej Hantoush**

- GitHub: [Murhej](https://github.com/Murhej)
- LinkedIn: [murhej-hantoush](https://www.linkedin.com/in/murhej-hantoush-928a90198/)
- Email: [murhej.hantoush.work@gmail.com](mailto:murhej.hantoush.work@gmail.com)
