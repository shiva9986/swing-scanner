import pandas as pd

print("Loading bhavcopy...")

# Load file
df = pd.read_csv("data/bhavcopy.csv")

print("Columns found:", df.columns.tolist())

# Convert required numeric columns
numeric_cols = [
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER",
    "HIGH_PRICE"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with missing values
df = df.dropna(subset=numeric_cols)

print("Total stocks:", len(df))

# === SIMPLE SWING LOGIC ===
filtered = df[
    (df["CLOSE_PRICE"] > 100) &
    (df["TTL_TRD_QNTY"] > 500000) &
    (df["DELIV_PER"] > 50)
]

print("Filtered stocks:", len(filtered))

# Save output
filtered.to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully ✅")
