import pandas as pd

# Load bhavcopy
df = pd.read_csv("bhavcopy.csv")

# Filter EQ series
df = df[df["SERIES"] == "EQ"]

# Convert numeric columns
cols = ["PREV_CLOSE", "OPEN_PRICE", "HIGH_PRICE",
        "LOW_PRICE", "CLOSE_PRICE",
        "TTL_TRD_QNTY", "DELIV_PER"]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=cols)

# -------------------------
# 1️⃣ Calculate Price Metrics
# -------------------------

df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

df["RANGE"] = df["HIGH_PRICE"] - df["LOW_PRICE"]

df["CLOSE_NEAR_HIGH"] = (df["HIGH_PRICE"] - df["CLOSE_PRICE"]) / df["HIGH_PRICE"]

# Normalize volume
df["VOL_SCORE"] = df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max() * 100

# -------------------------
# 2️⃣ Momentum Score
# -------------------------

df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 3 +
    df["VOL_SCORE"] * 1.5 +
    (1 - df["CLOSE_NEAR_HIGH"]) * 20
)

# -------------------------
# 3️⃣ Accumulation Score
# -------------------------

df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.7 +
    df["VOL_SCORE"] * 1.2 +
    (1 - df["CLOSE_NEAR_HIGH"]) * 15
)

# -------------------------
# 4️⃣ Institutional Score
# -------------------------

df["INSTITUTIONAL_SCORE"] = (
    df["MOMENTUM_SCORE"] * 0.5 +
    df["ACCUMULATION_SCORE"] * 0.5
)

# Remove penny / junk stocks
df = df[df["CLOSE_PRICE"] > 20]

# Sort by Institutional Score
df = df.sort_values("INSTITUTIONAL_SCORE", ascending=False)

# Select Top 15
top15 = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "VOL_SCORE",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "INSTITUTIONAL_SCORE"
]].head(15)

# Save output
top15.to_excel("swing_output.xlsx", index=False)

print("Professional Cash Scanner Completed Successfully.")
