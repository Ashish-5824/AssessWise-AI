from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import faiss
import pickle
from sentence_transformers import SentenceTransformer

app = FastAPI(title="AssessWise AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and metadata
index = faiss.read_index("shl_index.faiss")

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

class JDRequest(BaseModel):
    job_description: str
    top_k: int = 5

@app.post("/recommend")
def recommend(req: JDRequest):
    emb = model.encode([req.job_description])
    _, idxs = index.search(emb, req.top_k)

    results = []
    for i in idxs[0]:
        results.append({
            "assessment_name": metadata[i]["Assessment Name"],
            "assessment_url": metadata[i]["Assessment URL"],
            "matched_text": metadata[i]["text"],
            "estimated_time": "20–30 minutes"
        })

    return {"recommended_assessments": results}