import { useState } from "react";
import logo from "../assets/logo.png";
import "./mainpage.css";

function Mainpage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [confidence, setConfidence] = useState("");
  const [medicineInfo, setMedicineInfo] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [funFact, setFunFact] = useState("");

  // ✅ Handle file selection + preview
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setPrediction("");
    setConfidence("");
    setMedicineInfo(null);
    setErrorMsg("");
    setFunFact("");

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };

  // ✅ Send image to backend + fetch medicine safety
  const handlePredict = async () => {
    if (!selectedFile) {
      alert("Please select an image first.");
      return;
    }

    setLoading(true);
    setErrorMsg("");
    setMedicineInfo(null);
    setFunFact("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      // ✅ OCR Prediction
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setPrediction(data.prediction);
      setConfidence((data.confidence * 100).toFixed(2) + "%");

      // ✅ Fetch medicine safety info
      const medRes = await fetch(
        `http://127.0.0.1:8000/medicine/${data.prediction}`
      );

      const medData = await medRes.json();

      if (medData.error) {
        setMedicineInfo(null);
        setFunFact("");
        setErrorMsg("⚠️ No safety data found for this medicine.");
      } else {
        setMedicineInfo(medData.safety_info || null);

        // ✅ Fun Fact Auto-Generator
        setFunFact(
          `Did you know? ${data.prediction} is among the most commonly prescribed medications worldwide.`
        );
      }
    } catch (error) {
      console.error("Prediction error:", error);
      alert("❌ Backend connection failed.");
    }

    setLoading(false);
  };

  return (
    <div className="mainpage">
      {/* ---------- HEADER ---------- */}
      <header className="Header">
        <img src={logo} alt="Logo" />
        <h2>Prescription Recognition System</h2>
      </header>

      {/* ---------- BODY ---------- */}
      <div className="bodys">
        <div className="box">
          <h1>Upload Prescription Image</h1>

          <input type="file" className="inpute" onChange={handleFileChange} />

          {preview && (
            <div className="preview-container">
              <img src={preview} alt="Preview" className="preview-image" />
            </div>
          )}

          <button className="predict-btn" onClick={handlePredict}>
            {loading ? "Predicting..." : "Run Prediction"}
          </button>

          {/* ✅ MEDICAL DISCLAIMER ✅ */}
          <p className="disclaimer">
            ⚠️ This system is for educational purposes only and must NOT be used
            for medical diagnosis or treatment. Always consult a licensed
            doctor or pharmacist.
          </p>

          {/* ✅ OCR RESULT */}
          {prediction && (
            <div className="result-box">
              <p><b>Prediction:</b> {prediction}</p>
              <p><b>Confidence:</b> {confidence}</p>
            </div>
          )}

          {/* ✅ MEDICINE SAFETY POPUP MODAL */}
          {medicineInfo && (
            <div
              className="modal-overlay"
              onClick={() => setMedicineInfo(null)}
            >
              <div
                className="modal-card"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  className="modal-close"
                  onClick={() => setMedicineInfo(null)}
                >
                  ✕
                </button>

                <h2>{prediction} — Safety Information</h2>

                {Object.entries(medicineInfo).map(([key, value]) => (
                  <p key={key}>
                    <b>{key.replaceAll("_", " ")}:</b> {value}
                  </p>
                ))}

                {/* ✅ FUN FACT SECTION ✅ */}
                {funFact && (
                  <div className="fun-fact">
                    <h4>🧠 Fun Fact</h4>
                    <p>{funFact}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* ✅ ERROR MESSAGE */}
          {errorMsg && <p className="error">{errorMsg}</p>}
        </div>
      </div>

      {/* ---------- FOOTER ---------- */}
      <footer className="footer">
        <p>© 2025 Murhej Hantoush | AI Prescription Recognition</p>
      </footer>
    </div>
  );
}

export default Mainpage;
