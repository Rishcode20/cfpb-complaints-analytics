import pandas as pd
df = pd.read_csv("data/complaints.csv")
print(df.shape)
print(df.columns.tolist())
narr = df["Consumer complaint narrative"].dropna()
print("rows with narrative:", len(narr))
print(narr.iloc[0][:500])