import pandas as pd
from datetime import datetime

print("🚀 Starting NSE Swing Scanner...")

# ==========================
# 1️⃣ Load Bhavcopy
# ==========================
try:
    df = pd.read_csv("data/bhavcopy.csv")
    print("✅ Bhavcopy Loaded Successfully")
except Exception as e:
    print("❌ Error loading bhavcopy:", e)
    exit()

# ==========================
# 2️⃣ Clean Data
# ==========================
df.columns = df.columns.str.strip()

numeric_cols = [
    "OPEN_PRICE",
    "HIGH_PRICE",
    "LOW_PRICE",
    "CLOSE_PRICE",
    "TOTTRDQTY",
    "DELIV_QTY",
    "DELIV_PER"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# ==========================
# 3️⃣ Professional Filters
# ==========================

# High Volume (Above 20-day type logic approximation)
volume_filter = df["TOTTRDQTY"] > df["TOTTRDQTY"].mean()

# Strong Delivery
delivery_filter = df["DELIV_PER"] > 40

# Price Above 100
price_filter = df["CLOSE_PRICE"] > 100

# Bullish Candle
candle_filter = df["CLOSE_PRICE"] > df["OPEN_PRICE"]

# Combine
scanner = df[
    volume_filter &
    delivery_filter &
    price_filter &
    candle_filter
]

# ==========================
# 4️⃣ Sort By Delivery %
# ==========================
scanner = scanner.sort_values(by="DELIV_PER", ascending=False)

# ==========================
# 5️⃣ Save Output
# ==========================
today = datetime.now().strftime("%d-%m-%Y")
output_file = f"output_swing_{today}.csv"

scanner.to_csv(output_file, index=False)

print("🎯 Scanner Completed")
print("📊 Stocks Found:", len(scanner))
print("📁 Output File Created:", output_file)
