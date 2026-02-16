import pandas as pd

print("Loading bhavcopy...")

# Read CSV
df = pd.read_csv("data/bhavcopy.csv")

# Remove extra spaces in column names
df.columns = df.columns.str.strip()

print("Columns detected:", df.columns.tolist())

# Filter EQ only if column exists
if "SERIES" in df.columns:
    df = df[df["SERIES"].str.strip() == "EQ"]
else:
    print("SERIES column not found!")

# Convert required columns safely
numeric_cols = ["CLOSE_PRICE", "PREV_CLOSE", "DELIV_PER", "TTL_TRD_QNTY"]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"{col} not found in file!")

# Drop missing rows
df = df.dropna(subset=["CLOSE_PRICE", "PREV_CLOSE", "DELIV_PER", "TTL_TRD_QNTY"])

# =============================
# Momentum Score
# =============================

df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 3 +
    (df["TTL_TRD_QNTY"] / 100000)
)

# =============================
# Accumulation Score
# =============================

df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 1.5 +
    (df["TTL_TRD_QNTY"] / 200000)
)

# =============================
# Final Score
# =============================

df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# Sort
df = df.sort_values("FINAL_SCORE", ascending=False)

# Take Top 10
top10 = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]].head(10)

# Save output
top10.to_excel("swing_output.xlsx", index=False)

print("Top 10 stocks generated successfully!")
