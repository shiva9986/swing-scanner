import pandas as pd

# Load file
df = pd.read_csv("data/bhavcopy.csv")

# Clean column names
df.columns = df.columns.str.strip()

print("Columns found:", df.columns)

# Filter EQ only (if column exists)
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]

# Convert numeric safely
for col in ["CLOSE_PRICE", "DELIV_PER", "TTL_TRD_QNTY"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# Momentum score
df["MOMENTUM_SCORE"] = df["CLOSE_PRICE"].pct_change() * 100

# Accumulation score
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.4 +
    (df["TTL_TRD_QNTY"] / 100000) * 0.6
)

df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

top10 = df.sort_values("FINAL_SCORE", ascending=False).head(10)

top10.to_excel("swing_output.xlsx", index=False)

print("Scanner completed.")
