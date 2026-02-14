import pandas as pd

# Load bhavcopy
df = pd.read_csv("data/bhavcopy.csv")

print("Columns found in file:")
print(df.columns)

print("\nTotal rows:", len(df))

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns safely
numeric_cols = [
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Basic filter (very simple test)
result = df[df["SERIES"] == "EQ"]

print("EQ Stocks count:", len(result))

# Save output
result.to_excel("swing_output.xlsx", index=False)

print("File created successfully!")
