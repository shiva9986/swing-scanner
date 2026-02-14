import pandas as pd
import os

# ===============================
# CONFIGURATION
# ===============================

DATA_PATH = "data/bhavcopy.csv"   # Your uploaded bhavcopy location
OUTPUT_FILE = "swing_output.xlsx"

# ===============================
# LOAD DATA
# ===============================

print("Loading bhavcopy...")

df = pd.read_csv(DATA_PATH)

# Convert numeric columns safely
numeric_cols = [
    "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE",
    "CLOSE_PRICE", "PREV_CLOSE",
    "TOTTRDQTY", "DELIV_PER"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# ===============================
# BASIC PROFESSIONAL FILTERS
# ===============================

print("Applying filters...")

# 1️⃣ Price above 100
price_filter = df["CLOSE_PRICE"] > 100

# 2️⃣ Volume above 20-day average (temporary proxy using mean)
volume_filter = df["TOTTRDQTY"] > df["TOTTRDQTY"].mean()

# 3️⃣ Strong delivery
delivery_filter = df["DELIV_PER"] > 40

# 4️⃣ Strong candle (Close > Prev Close)
momentum_filter = df["CLOSE_PRICE"] > df["PREV_CLOSE"]

# Combine filters
filtered = df[
    price_filter &
    volume_filter &
    delivery_filter &
    momentum_filter
]

# ===============================
# ADD SCORE SYSTEM (Professional Edge)
# ===============================

filtered["Score"] = (
    (filtered["CLOSE_PRICE"] > filtered["OPEN_PRICE"]).astype(int) +
    (filtered["DELIV_PER"] > 50).astype(int) +
    (filtered["TOTTRDQTY"] > filtered["TOTTRDQTY"].mean()).astype(int)
)

filtered = filtered.sort_values(by="Score", ascending=False)

# ===============================
# SAVE OUTPUT
# ===============================

print("Saving results...")

filtered.to_excel(OUTPUT_FILE, index=False)

print("Done. File saved as:", OUTPUT_FILE)
