import pandas as pd

# -----------------------------
# 1. Load Bhavcopy
# -----------------------------
df = pd.read_csv("bhavcopy.csv")   # make sure file name matches exactly

# -----------------------------
# 2. Filter Only EQ Series
# -----------------------------
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]

# -----------------------------
# 3. Convert Required Columns
# -----------------------------
numeric_cols = [
    "PREV_CLOSE",
    "CLOSE_PRICE",
    "DELIV_PER",
    "TTL_TRD_QNTY"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)

# -----------------------------
# 4. Calculate % Change
# -----------------------------
df["PCT_CHANGE"] = (
    (df["CLOSE_PRICE"] - df["PREV_CLOSE"]) 
    / df["PREV_CLOSE"]
) * 100

# -----------------------------
# 5. MOMENTUM SCORE
# Price Strength + Volume
# -----------------------------
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 2 +
    (df["TTL_TRD_QNTY"] / 1000000)
)

# -----------------------------
# 6. ACCUMULATION SCORE
# Delivery + Volume Stability
# -----------------------------
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.5 +
    (df["TTL_TRD_QNTY"] / 2000000)
)

# -----------------------------
# 7. FINAL COMBINED SCORE
# -----------------------------
df["FINAL_SCORE"] = (
    df["MOMENTUM_SCORE"] * 0.6 +
    df["ACCUMULATION_SCORE"] * 0.4
)

# -----------------------------
# 8. Sort & Select Top 10
# -----------------------------
top10 = df.sort_values("FINAL_SCORE", ascending=False).head(10)

# -----------------------------
# 9. Select Output Columns
# -----------------------------
output = top10[
    [
        "SYMBOL",
        "CLOSE_PRICE",
        "PCT_CHANGE",
        "DELIV_PER",
        "TTL_TRD_QNTY",
        "MOMENTUM_SCORE",
        "ACCUMULATION_SCORE",
        "FINAL_SCORE"
    ]
]

# -----------------------------
# 10. Save Output
# -----------------------------
output.to_excel("swing_output.xlsx", index=False)

print("Top 10 Stocks Generated Successfully ✅")
