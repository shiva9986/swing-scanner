import pandas as pd

# -------------------------------
# 1️⃣ LOAD BHAVCOPY
# -------------------------------

df = pd.read_csv("data/bhavcopy.csv")

# Standardize column names (remove spaces)
df.columns = df.columns.str.strip()

# Keep only EQ series
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]

# -------------------------------
# 2️⃣ CONVERT REQUIRED COLUMNS
# -------------------------------

numeric_cols = [
    "CLOSE_PRICE",
    "PREV_CLOSE",
    "DELIV_PER",
    "TTL_TRD_QNTY"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["CLOSE_PRICE", "PREV_CLOSE"])

# -------------------------------
# 3️⃣ CALCULATE % CHANGE
# -------------------------------

df["PCT_CHANGE"] = (
    (df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]
) * 100

# -------------------------------
# 4️⃣ MOMENTUM SCORE
# (Price strength + Volume strength)
# -------------------------------

df["MOMENTUM_SCORE"] = (
    (df["PCT_CHANGE"] * 2) +
    (df["TTL_TRD_QNTY"] / 1_000_000)
)

# -------------------------------
# 5️⃣ ACCUMULATION SCORE
# (Delivery + Volume)
# -------------------------------

df["ACCUMULATION_SCORE"] = (
    (df["DELIV_PER"] * 1.5) +
    (df["TTL_TRD_QNTY"] / 2_000_000)
)

# -------------------------------
# 6️⃣ FINAL SCORE (Weighted)
# -------------------------------

df["FINAL_SCORE"] = (
    df["MOMENTUM_SCORE"] * 0.6 +
    df["ACCUMULATION_SCORE"] * 0.4
)

# -------------------------------
# 7️⃣ SORT & TAKE TOP 20
# -------------------------------

df = df.sort_values("FINAL_SCORE", ascending=False)

output = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]].head(20)

# -------------------------------
# 8️⃣ SAVE OUTPUT
# -------------------------------

output.to_excel("swing_output.xlsx", index=False)

print("✅ Scanner Completed Successfully")
