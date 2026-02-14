import pandas as pd

# Load bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

# Clean column names (very important)
df.columns = df.columns.str.strip()

# Clean SERIES column
df["SERIES"] = df["SERIES"].astype(str).str.strip()

# Filter only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert numeric columns safely
numeric_cols = ["CLOSE_PRICE", "PREV_CLOSE", "DELIV_PER", "TTL_TRD_QNTY"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop rows where required values missing
df = df.dropna(subset=numeric_cols)

# Calculate % change
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# Remove negative moves (optional but good for swing)
df = df[df["PCT_CHANGE"] > 0]

# Score system
df["SCORE"] = (
    df["PCT_CHANGE"] * 2 +
    df["DELIV_PER"] * 0.3 +
    (df["TTL_TRD_QNTY"] / 100000)
)

# Sort by score
df = df.sort_values("SCORE", ascending=False)

# Take Top 10
top10 = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "SCORE"
]].head(10)

# Save output
top10.to_excel("swing_output.xlsx", index=False)

print("Top 10 stocks generated successfully.")
