import re
import numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv("data/complaints.csv")
df = df.dropna(subset=["Consumer complaint narrative"])
df = df.sample(n=min(15000, len(df)), random_state=42).reset_index(drop=True)
df["text"] = df["Consumer complaint narrative"].apply(
    lambda t: re.sub(r"X{2,}", "", t)[:1000]
)
df.to_csv("data/sample.csv", index=False)
print("complaints:", len(df))

model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(df["text"].tolist(), batch_size=64,
                   show_progress_bar=True, normalize_embeddings=True)
np.save("data/embeddings.npy", emb)

for k in [6, 8, 10, 12, 15]:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(emb)
    s = silhouette_score(emb, km.labels_, sample_size=5000, random_state=42)
    print("K =", k, "silhouette =", round(s, 3))