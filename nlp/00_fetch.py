import sys, time
import requests
import pandas as pd

product = sys.argv[1]
start = sys.argv[2] if len(sys.argv) > 2 else "2025-01-01"

URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
rows = []
for frm in range(0, 10000, 500):
    r = requests.get(
        URL,
        params={
            "has_narrative": "true",
            "product": product,
            "date_received_min": start,
            "size": 500,
            "frm": frm,
            "sort": "created_date_desc",
            "field": "all",
        },
                headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
            "Accept": "application/json",
        },
        timeout=60,
    )
    r.raise_for_status()
    hits = r.json()["hits"]["hits"]
    if not hits:
        break
    for h in hits:
        s = h["_source"]
        rows.append({
            "Date received": s.get("date_received"),
            "Product": s.get("product"),
            "Issue": s.get("issue"),
            "Company": s.get("company"),
            "Consumer complaint narrative": s.get("complaint_what_happened"),
        })
    print("fetched", len(rows))
    time.sleep(0.5)

df = pd.DataFrame(rows)
df.to_csv("data/complaints.csv", index=False)
print(df.shape)
print(df["Consumer complaint narrative"].notna().sum(), "with narrative")