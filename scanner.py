import pandas as pd

print("Loading bhavcopy...")

# Auto-detect separator
try:
    df = pd.read_csv("data/bhavcopy.csv")
except:
    df = pd.read_csv("data/bhavcopy.csv", sep=";")

print("Columns in file:")
print(df.columns)

# Remove spaces in column names
df.columns = df.columns.str.strip()

# Keep only EQ series
if "SERIES" in df.columns:
    df = df[df["SERIES"] == "EQ"]
else:
    print("SERIES column not found!")
    exit()

# Convert required columns
num_cols = ["CLOSE_PRICE", "PREV_CLOSE", "DELIV_PER", "TTL_TRD_QNTY"]

for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        print(f"{col} not found in file!")
        exit()

df = df.dropna(subset=num_cols)

# =========================
# MOMENTUM SCORE
# =========================
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 2 +
    (df["TTL_TRD_QNTY"] / 1000000)
)

# =========================
# ACCUMULATION SCORE
# =========================
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.7 +
    (df["TTL_TRD_QNTY"] / 2000000)
)

# =========================
# FINAL SORT
# =========================
df = df.sort_values("MOMENTUM_SCORE", ascending=False)

top10 = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE"
]].head(10)

top10.to_excel("swing_output.xlsx", index=False)

print("Top 10 stocks generated successfully.")
