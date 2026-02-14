import pandas as pd

# Load bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

# Clean column names (remove spaces if any)
df.columns = df.columns.str.strip()

# Convert required columns to numeric
numeric_cols = [
    "PREV_CLOSE",
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Basic Swing Conditions
df["PRICE_CHANGE_%"] = ((df["CLOSE_PRICE"] - df["PREV_CLOSE"]) / df["PREV_CLOSE"]) * 100

filtered = df[
    (df["PRICE_CHANGE_%"] > 1) & 
    (df["DELIV_PER"] > 40) &
    (df["TTL_TRD_QNTY"] > 50000)
]

# Sort by best movers
filtered = filtered.sort_values(by="PRICE_CHANGE_%", ascending=False)

# Save output
filtered.to_excel("swing_output.xlsx", index=False)

print("Scan completed successfully.")
print("Stocks found:", len(filtered))
