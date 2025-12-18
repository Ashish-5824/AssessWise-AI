import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer

df = pd.read_csv("data/Gen_AI_Dataset.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/shl_index.faiss")

with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

hits = 0
for _, row in df.iterrows():
    emb = model.encode([row["query"]])
    _, idxs = index.search(emb, 10)
    urls = [metadata[i]["assessment_url"] for i in idxs[0]]
    if row["assessment_url"] in urls:
        hits += 1

print("Recall@10:", hits / len(df))