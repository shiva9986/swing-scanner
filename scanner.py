import pandas as pd

# -----------------------------
# LOAD BHAVCOPY
# -----------------------------
df = pd.read_csv("data/bhavcopy.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Print columns for debugging (optional)
print("Available Columns:", df.columns.tolist())

# -----------------------------
# FILTER ONLY EQ SERIES
# -----------------------------
df = df[df["SERIES"] == "EQ"]

# -----------------------------
# CONVERT REQUIRED COLUMNS TO NUMERIC
# -----------------------------
numeric_cols = [
    "CLOSE_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# SIMPLE SWING CONDITIONS
# -----------------------------
df["Price_Up"] = df["CLOSE_PRICE"] > df["PREV_CLOSE"]
df["High_Volume"] = df["TTL_TRD_QNTY"] > df["TTL_TRD_QNTY"].mean()
df["Good_Delivery"] = df["DELIV_PER"] > 40

# Final selection
swing_stocks = df[
    df["Price_Up"] &
    df["High_Volume"] &
    df["Good_Delivery"]
]

# -----------------------------
# OUTPUT
# -----------------------------
output_cols = [
    "SYMBOL",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

swing_stocks[output_cols].to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully.")
