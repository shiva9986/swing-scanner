import pandas as pd

# ==============================
# 1️⃣ Load Bhavcopy
# ==============================

file_path = "data/bhavcopy.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Convert numeric columns
numeric_cols = [
    "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE", "CLOSE_PRICE",
    "TTL_TRD_QNTY", "DELIV_QTY", "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==============================
# 2️⃣ Professional Filters
# ==============================

# Filter 1: Price > 100 (avoid junk stocks)
price_filter = df["CLOSE_PRICE"] > 100

# Filter 2: Strong Volume (above average)
volume_filter = df["TTL_TRD_QNTY"] > df["TTL_TRD_QNTY"].mean()

# Filter 3: Strong Delivery (> 40%)
delivery_filter = df["DELIV_PER"] > 40

# Filter 4: Bullish Close (closing near high)
range_value = df["HIGH_PRICE"] - df["LOW_PRICE"]
bullish_close = (df["CLOSE_PRICE"] - df["LOW_PRICE"]) / range_value > 0.6

# Combine All Filters
scanner = df[
    price_filter &
    volume_filter &
    delivery_filter &
    bullish_close
]

# Select Important Columns
scanner = scanner[[
    "SYMBOL",
    "CLOSE_PRICE",
    "TTL_TRD_QNTY",
    "DELIV_PER"
]]

# Sort by Delivery %
scanner = scanner.sort_values(by="DELIV_PER", ascending=False)

# ==============================
