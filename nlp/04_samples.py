import pandas as pd

df = pd.read_csv("data/clustered.csv")
for c in sorted(df.cluster.unique()):
    sub = df[df.cluster == c]
    print("=" * 60)
    print("CLUSTER", c, "| size", len(sub))
    print("KEYWORDS:", sub.keywords.iloc[0])
    for t in sub.sample(4, random_state=1).text:
        print("-", t[:300].replace("\n", " "))