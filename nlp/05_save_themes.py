import pandas as pd

titles = {
    0: "Identity theft and credit report removal",
    1: "Refunds and merchant disputes",
    2: "Rewards, bonuses and promotional offers",
    3: "Fraud and unauthorized charge disputes",
    4: "Citibank disputes, closures and payments",
    5: "Account opening and card delivery problems",
    6: "Deferred interest and billing errors",
    7: "Capital One account restrictions and closures",
    8: "Credit reporting errors and legal-style disputes",
    9: "Late fees, payments and interest charges",
}

df = pd.read_csv("data/clustered.csv")
out = (df.groupby("cluster").size().rename("size").reset_index())
out["title"] = out.cluster.map(titles)
out["share_pct"] = (out["size"] / out["size"].sum() * 100).round(1)
out.to_csv("data/themes.csv", index=False)
print(out.sort_values("size", ascending=False).to_string(index=False))