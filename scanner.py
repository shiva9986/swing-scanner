import pandas as pd

print("Reading Bhavcopy...")

# Read CSV
df = pd.read_csv("data/bhavcopy.csv")

# Clean column names (remove spaces)
df.columns = df.columns.str.strip()

print("Columns Found:", df.columns.tolist())

# Remove spaces in SERIES column
df["SERIES"] = df["SERIES"].astype(str).str.strip()

# Keep only EQ stocks
df = df[df["SERIES"] == "EQ"]

print("Stocks after EQ filter:", len(df))

# Convert numeric columns safely
numeric_cols = [
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Basic swing filter
df = df[
    (df["CLOSE_PRICE"] > 100) &
    (df["TTL_TRD_QNTY"] > 500000) &
    (df["DELIV_PER"] > 40)
]

print("Stocks after swing filter:", len(df))

# Save output
df.to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully.")
