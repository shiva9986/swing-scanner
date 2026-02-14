import pandas as pd

# Load bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

# Keep only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert numeric columns
numeric_cols = [
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Filters
price_filter = df["CLOSE_PRICE"] > 100
volume_filter = df["TTL_TRD_QNTY"] > df["TTL_TRD_QNTY"].mean()
delivery_filter = df["DELIV_PER"] > 40

# Apply filters
scanner = df[price_filter & volume_filter & delivery_filter]

# Select output columns
output = scanner[[
    "SYMBOL",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]]

# Save output
output.to_excel("swing_output.xlsx", index=False)

print("Scanner completed successfully.")
