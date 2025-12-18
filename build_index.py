import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# 1. Load CSV
df = pd.read_csv("shl_catalogue.csv")

# 2. Create text column
df["text"] = (
    df["Assessment Name"].astype(str) + " | " +
    df["Assessment URL"].astype(str)
)

# 3. Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 4. Generate embeddings
embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

# 5. Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# 6. Save index + metadata
faiss.write_index(index, "shl_index.faiss")

with open("metadata.pkl", "wb") as f:
    pickle.dump(df.to_dict("records"), f)

print("✅ Index and metadata created successfully")