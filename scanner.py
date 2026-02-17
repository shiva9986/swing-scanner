import pandas as pd

print("Loading Bhavcopy...")

# Load file
df = pd.read_csv("data/bhavcopy.csv")

print("Rows loaded:", len(df))
print("Columns found:", df.columns.tolist())

# Clean column names
df.columns = df.columns.str.strip().str.upper()

# Ensure required columns exist
required_cols = ["SYMBOL", "SERIES", "CLOSE_PRICE", "PREV_CLOSE", "TTL_TRD_QNTY", "DELIV_PER"]

for col in required_cols:
    if col not in df.columns:
        print(f"Missing column: {col}")
        exit()

# Filter only EQ series safely
df = df[df["SERIES"] == "EQ"].copy()

print("EQ Rows:", len(df))

if len(df) == 0:
    print("No EQ stocks found. Exiting.")
    exit()

# Convert numeric columns
df["CLOSE_PRICE"] = pd.to_numeric(df["CLOSE_PRICE"], errors="coerce")
df["PREV_CLOSE"] = pd.to_numeric(df["PREV_CLOSE"], errors="coerce")
df["TTL_TRD_QNTY"] = pd.to_numeric(df["TTL_TRD_QNTY"], errors="coerce")
df["DELIV_PER"] = pd.to_numeric(df["DELIV_PER"], errors="coerce")

# Calculate Percent Change
df["PCT_CHANGE"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

# Drop invalid rows
df = df.dropna(subset=["PCT_CHANGE", "TTL_TRD_QNTY", "DELIV_PER"])

print("Valid rows after cleaning:", len(df))

if len(df) == 0:
    print("No valid data after cleaning. Exiting.")
    exit()

# --- SCORING ---

# Momentum Score
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 0.6 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 100 * 0.4
)

# Accumulation Score
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 0.7 +
    (df["TTL_TRD_QNTY"] / df["TTL_TRD_QNTY"].max()) * 100 * 0.3
)

# Final Score
df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# Sort
df = df.sort_values("FINAL_SCORE", ascending=False)

# Select top 50
output = df[[
    "SYMBOL",
    "CLOSE_PRICE",
    "PCT_CHANGE",
    "DELIV_PER",
    "TTL_TRD_QNTY",
    "MOMENTUM_SCORE",
    "ACCUMULATION_SCORE",
    "FINAL_SCORE"
]].head(50)

# Save output
output.to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully!")
