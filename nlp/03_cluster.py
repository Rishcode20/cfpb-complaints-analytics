import sys
import numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

K = int(sys.argv[1])
df = pd.read_csv("data/sample.csv")
emb = np.load("data/embeddings.npy")

km = KMeans(n_clusters=K, n_init=10, random_state=42).fit(emb)
df["cluster"] = km.labels_

extra = {"credit", "card", "account", "accounts", "bank", "did", "just", "year"}
tfidf = TfidfVectorizer(
    stop_words=list(ENGLISH_STOP_WORDS | extra),
    token_pattern=r"[A-Za-z]{3,}",
    ngram_range=(1, 2),
    min_df=30,
    max_df=0.4,
)
X = tfidf.fit_transform(df["text"])
terms = np.array(tfidf.get_feature_names_out())

top = {}
for c in range(K):
    mean = np.asarray(X[(df.cluster == c).values].mean(axis=0)).ravel()
    top[c] = ", ".join(terms[mean.argsort()[-8:][::-1]])
df["keywords"] = df.cluster.map(top)
df.to_csv("data/clustered.csv", index=False)

print(df.cluster.value_counts().sort_index())
for c in range(K):
    print(c, top[c])

ct = pd.crosstab(df.cluster, df["Issue"])
print("Agreement with CFPB Issue labels:",
      round(ct.max(axis=1).sum() / ct.values.sum(), 3))