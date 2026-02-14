import pandas as pd

# Load bhavcopy exactly as NSE gives
df = pd.read_csv("data/bhavcopy.csv")

# Clean column names (remove spaces if any)
df.columns = df.columns.str.strip()

# Convert required numeric columns
numeric_cols = [
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove BE series (only EQ stocks)
df = df[df["SERIES"] == "EQ"]

# Basic swing conditions (mild filter)
filtered = df[
    (df["TTL_TRD_QNTY"] > 100000) &
    (df["DELIV_PER"] > 30)
]

# Select important columns
result = filtered[[
    "SYMBOL",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]]

# Sort by delivery %
result = result.sort_values(by="DELIV_PER", ascending=False)

# Save output
result.to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully.")
