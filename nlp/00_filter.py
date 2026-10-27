import sys
import pandas as pd

cols = ["Date received", "Product", "Issue", "Company",
        "Consumer complaint narrative"]
df = pd.read_csv("data/narr_2026.csv", usecols=cols)
print("total rows:", len(df))

has = df[df["Consumer complaint narrative"].notna()]
print("rows with narrative:", len(has))
print(has["Product"].value_counts().head(10))

if len(sys.argv) > 1:
    out = has[has["Product"] == sys.argv[1]]
    out.to_csv("data/complaints.csv", index=False)
    print("saved", out.shape, "to data/complaints.csv")