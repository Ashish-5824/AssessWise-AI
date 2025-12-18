import { useState } from "react";

export default function App() {
  const [jd, setJd] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeJD = async () => {
    if (!jd.trim()) return;

    setLoading(true);
    const res = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        job_description: jd,
        top_k: 5,
      }),
    });

    const data = await res.json();
    setResults(data.recommended_assessments || []);
    setLoading(false);
  };

  return (
    <div style={{ fontFamily: "Arial", padding: "40px", background: "#f5f5f5" }}>
      <h1 style={{ textAlign: "center" }}>
        AI-Powered Assessment Recommendation Engine
        <br /> using SHL Product Catalogue
      </h1>

      <p style={{ textAlign: "center", color: "#666" }}>
        Paste a job description and instantly receive AI-driven recommendations
      </p>

      <div style={{ display: "flex", gap: "30px", marginTop: "40px" }}>
        {/* LEFT PANEL */}
        <div style={{ width: "30%" }}>
          <h3>Job Description</h3>
          <textarea
            rows="10"
            style={{ width: "100%", padding: "10px" }}
            placeholder="Paste job description here..."
            value={jd}
            onChange={(e) => setJd(e.target.value)}
          />
          <button
            onClick={analyzeJD}
            style={{
              marginTop: "15px",
              width: "100%",
              padding: "12px",
              background: "#6b46c1",
              color: "#fff",
              border: "none",
              cursor: "pointer",
              fontSize: "16px",
            }}
          >
            Analyze & Recommend
          </button>
        </div>

        {/* RIGHT PANEL */}
        <div style={{ width: "70%" }}>
          <h3>Recommended Assessments</h3>

          {loading && <p>Analyzing...</p>}

          {results.map((item, idx) => (
            <div
              key={idx}
              style={{
                background: "#fff",
                padding: "20px",
                marginBottom: "15px",
                borderRadius: "8px",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            >
              <h4 style={{ color: "#6b46c1" }}>
                <a href={item.assessment_url} target="_blank">
                  {item.assessment_name}
                </a>
              </h4>
              <p>
                <b>Purpose:</b> {item.purpose}
              </p>
              <p>
                <b>Estimated Time:</b> {item.estimated_time}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}