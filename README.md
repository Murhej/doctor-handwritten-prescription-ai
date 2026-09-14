<div align="center">

# 🩺 Doctor Handwritten Prescription AI

### AI-powered prescription handwriting recognition with a clean full-stack web experience

Turn difficult-to-read handwritten prescription images into clearer, structured digital text using AI, OCR, and image-processing techniques.

<br>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![JavaScript](https://img.shields.io/badge/JavaScript-Web_App-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![AI](https://img.shields.io/badge/AI-Handwriting_Recognition-7B61FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Portfolio_Project-success?style=for-the-badge)

<br>

[Overview](#-overview) •
[Features](#-features) •
[How It Works](#-how-it-works) •
[Tech Stack](#-tech-stack) •
[Installation](#-installation) •
[Challenges](#-technical-challenges) •
[Future Improvements](#-future-improvements)

</div>

---

## 🌟 Overview

**Doctor Handwritten Prescription AI** is a full-stack AI project built to explore one of the most difficult real-world OCR problems: interpreting handwritten medical prescriptions.

The application allows a user to upload a prescription image, sends it to a Python backend for processing, applies image-processing and recognition techniques, and returns a more readable digital result through a web interface.

This project was created as a practical AI/software-development portfolio project focused on combining:

- artificial intelligence
- OCR and handwriting recognition
- image preprocessing
- backend API development
- frontend development
- real-world problem solving

---

## 🎯 The Problem

Handwritten prescriptions can be difficult to interpret because handwriting varies significantly between people.

Recognition becomes even more difficult when an image contains:

- unclear handwriting
- abbreviations
- unusual medication names
- poor lighting
- low resolution
- shadows or blur
- inconsistent spacing
- overlapping characters

Traditional OCR performs best on clean printed text, so handwritten prescriptions create a much harder recognition problem.

---

## 💡 Why I Built This Project

I wanted to build an AI project around a meaningful real-world problem rather than only training a model in isolation.

The main goals were to:

- explore how AI can interpret difficult handwriting
- understand the limitations of traditional OCR
- improve recognition through image preprocessing
- connect an AI-processing workflow to a usable web interface
- practice full-stack development
- design an application around a realistic user workflow

This project helped me move from **"building a model"** to **"building an AI-powered product."**

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 **Prescription Upload** | Upload a handwritten prescription image through the web interface |
| 🖼️ **Image Processing** | Prepare the uploaded image before recognition |
| 🤖 **AI / OCR Recognition** | Analyze handwritten text and attempt to extract readable content |
| 🔌 **Backend API** | Connect frontend requests to the Python processing pipeline |
| 🖥️ **Web Interface** | Provide a simple experience for uploading images and viewing results |
| 📄 **Readable Output** | Display extracted text in a clearer digital format |
| 🧩 **Full-Stack Integration** | Combine frontend, backend, and AI processing in one application |

---

## 🔄 How It Works

```text
┌──────────────────────┐
│ Prescription Image   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Frontend Upload      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Backend API          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Image Preprocessing  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ OCR / AI Recognition │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Extracted Text       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Result Display       │
└──────────────────────┘
```

### Application Flow

1. The user uploads a handwritten prescription image.
2. The frontend sends the image to the backend.
3. The backend prepares the image for analysis.
4. The recognition pipeline processes the handwriting.
5. Extracted or predicted text is returned.
6. The frontend displays the result to the user.

---

## 🧰 Tech Stack

### Frontend

- **React**
- **JavaScript**
- **HTML**
- **CSS**

### Backend

- **Python**
- Backend API for handling uploads and AI-processing requests

### AI / Computer Vision

- OCR-based text recognition
- handwriting recognition
- image preprocessing
- image-analysis workflow

> **Note:** Update this section with the exact AI and backend libraries used in the project if applicable, such as OpenCV, TensorFlow, PyTorch, Tesseract, EasyOCR, Flask, FastAPI, or similar tools.

---

## 📁 Project Structure

```text
doctor-handwritten-prescription-ai/
│
├── BackEnd/
│   └── backend application and AI-processing code
│
├── frontend/
│   └── React frontend application
│
└── README.md
```

For a cleaner long-term structure, the repository can later be standardized to:

```text
doctor-handwritten-prescription-ai/
│
├── backend/
├── frontend/
├── assets/
│   └── screenshots/
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🧠 Technical Challenges

### 1. Handwriting Variability

Printed text follows predictable shapes and spacing. Handwriting does not.

Different writing styles can drastically affect recognition quality, making handwritten prescriptions much harder than standard OCR tasks.

### 2. Image Quality

Recognition performance can change significantly depending on:

- lighting
- blur
- camera angle
- contrast
- shadows
- background noise
- image resolution

Preprocessing therefore becomes an important part of the recognition pipeline.

### 3. Medical Vocabulary

Medication names and medical terminology can contain uncommon words that standard OCR systems may not recognize well.

### 4. Frontend and Backend Integration

Another challenge was connecting the AI-processing workflow with a web interface so users could upload an image and receive a result through a simple application flow.

### 5. Reliability

A system working with medical text must clearly communicate uncertainty.

Because handwriting recognition is imperfect, this project is designed as an educational AI application rather than a medical decision-making system.

---

## 📚 What I Learned

Building this project strengthened my experience with:

- Python development
- JavaScript
- React
- frontend/backend integration
- API communication
- image preprocessing
- OCR concepts
- computer vision
- debugging full-stack applications
- designing AI workflows
- handling real-world input variability
- communicating AI limitations responsibly

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Murhej/doctor-handwritten-prescription-ai.git
cd doctor-handwritten-prescription-ai
```

### 2. Start the backend

```bash
cd BackEnd
pip install -r requirements.txt
python main.py
```

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm start
```

Then open the local development URL shown in your terminal.

---

## 🧪 Example Usage

### Input

Upload a photo or scanned image of a handwritten prescription.

### Processing

The image is sent through the backend recognition workflow.

### Output

The application returns extracted or predicted prescription text in a clearer, readable form.

---

## 📸 Screenshots

Add 2–4 screenshots here to make the repository much more attractive to recruiters.

Recommended screenshots:

1. **Home / Upload Screen**
2. **Prescription Uploaded**
3. **Recognition Result**
4. **Mobile or Responsive View**

Example:

```markdown
![Application Home](assets/screenshots/home.png)
![Recognition Result](assets/screenshots/result.png)
```

---

## 📊 Results & Evaluation

For a stronger AI portfolio project, add measurable performance results when available.

Useful metrics could include:

- OCR accuracy
- character error rate
- word error rate
- recognition confidence
- test-set accuracy
- processing time

Example format:

| Metric | Result |
|---|---:|
| Recognition Accuracy | Add result |
| Average Processing Time | Add result |
| Test Samples | Add result |

> Avoid adding performance claims unless they are measured from the project.

---

## 🔮 Future Improvements

Potential improvements include:

- improve handwriting-recognition accuracy
- add medication-name validation
- introduce confidence scores
- detect medication name, dosage, and frequency separately
- improve image preprocessing
- support multiple languages
- improve mobile responsiveness
- train on a larger handwriting dataset
- improve error handling
- add structured prescription output
- add model-performance evaluation

---

## ⚠️ Limitations

Handwritten medical-text recognition is a difficult AI problem.

The application may produce incorrect results when:

- handwriting is extremely unclear
- images are blurry
- lighting is poor
- characters overlap
- the prescription contains unusual abbreviations
- medication names are uncommon
- image quality is low

Any extracted result should be independently verified.

---

## 🛡️ Medical Disclaimer

> **This project is for educational, research, and portfolio purposes only.**

It is **not a certified medical device**.

Do not use the application's output to:

- identify medication without verification
- determine dosage
- change treatment
- make medical decisions
- replace consultation with a physician or pharmacist

Prescription information should always be verified by a qualified healthcare professional.

---

## 👨‍💻 Author

### Murhej

AI / Software Development Portfolio Project

GitHub: [@Murhej](https://github.com/Murhej)

---

<div align="center">

### ⭐ If you found this project interesting, consider starring the repository.

Built as a practical exploration of **AI + OCR + Full-Stack Development**.

</div>
