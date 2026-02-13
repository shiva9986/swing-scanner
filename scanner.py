import pandas as pd

print("🔥 NSE Professional Swing Scanner Starting...\n")

# Load Bhavcopy file
df = pd.read_csv("sec_bhavdata_full.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Filter only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert required columns to numeric
numeric_cols = ["CLOSE_PRICE", "TOTTRDQTY", "DELIV_PER"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Basic Filters (Professional Structure)

# 1️⃣ High Volume Stocks
volume_filter = df["TOTTRDQTY"] > df["TOTTRDQTY"].mean()

# 2️⃣ Strong Delivery
delivery_filter = df["DELIV_PER"] > 40

# 3️⃣ Price Above 100
price_filter = df["CLOSE_PRICE"] > 100

# Combine all filters
scanner = df[volume_filter & delivery_filter & price_filter]

# Sort by Delivery %
scanner = scanner.sort_values(by="DELIV_PER", ascending=False)

# Select Important Columns
final_output = scanner[[
    "SYMBOL",
    "CLOSE_PRICE",
    "TOTTRDQTY",
    "DELIV_PER"
]]

# Save Output
final_output.to_csv("scanner_output.csv", index=False)

print("✅ Scanner Completed!")
print("📁 Output file created: scanner_output.csv")
print("\nTop Results:\n")
print(final_output.head(15))
