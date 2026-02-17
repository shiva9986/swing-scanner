import pandas as pd

# ===============================
# LOAD BHAVCOPY
# ===============================

df = pd.read_csv("data/bhavcopy.csv")

print("Rows loaded:", len(df))
print("Columns found:", df.columns.tolist())

# ===============================
# CLEAN COLUMN NAMES
# ===============================

df.columns = df.columns.str.strip().str.upper()

# Keep only EQ series
df = df[df["SERIES"] == "EQ"]

# ===============================
# NUMERIC CONVERSION
# ===============================

numeric_cols = [
    "CLOSE_PRICE",
    "PREV_CLOSE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ===============================
# CALCULATIONS
# ===============================

df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# Momentum Score
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 2 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 100
)

# Accumulation Score
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 1.5 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 50
)

# Final Score
df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# ===============================
# SORT
# ===============================

df = df.sort_values("FINAL_SCORE", ascending=False)

# ===============================
# SAVE OUTPUT (IMPORTANT)
# ===============================

df.to_excel("swing_output.xlsx", index=False)

print("File saved successfully as swing_output.xlsx")
