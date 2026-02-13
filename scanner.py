import pandas as pd
import glob
import os

print("📊 Professional NSE Swing Scanner Running...\n")

# ---- AUTO DETECT LATEST CSV ----
csv_files = glob.glob("*.csv")

if not csv_files:
    print("❌ No CSV file found in directory.")
    exit()

latest_file = max(csv_files, key=os.path.getctime)

print(f"📁 Detected file: {latest_file}")

df = pd.read_csv(latest_file)

# ---- CLEAN DATA ----
df.columns = df.columns.str.strip()

# Keep only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert required columns safely
numeric_cols = [
    "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE",
    "CLOSE_PRICE", "TTL_TRD_QNTY",
    "DELIV_QTY", "DELIV_PER",
    "TURNOVER_LACS"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# ---- LIQUIDITY FILTER ----
df = df[df["TURNOVER_LACS"] > 500]

# ---- CLOSE STRENGTH ----
df["Close_Strength"] = (
    (df["CLOSE_PRICE"] - df["LOW_PRICE"]) /
    (df["HIGH_PRICE"] - df["LOW_PRICE"] + 0.0001)
)

# ---- BREAKOUT CANDIDATES ----
breakout = df[
    (df["Close_Strength"] > 0.7) &
    (df["DELIV_PER"] > 45)
].copy()

breakout["Score"] = (
    breakout["DELIV_PER"] * 0.6 +
    breakout["Close_Strength"] * 40
)

breakout = breakout.sort_values("Score", ascending=False)

# ---- ACCUMULATION CANDIDATES ----
accumulation = df[
    (df["DELIV_PER"] > 60) &
    (df["Close_Strength"] > 0.5)
].copy()

accumulation = accumulation.sort_values("DELIV_PER", ascending=False)

# ---- SAVE OUTPUT ----
with pd.ExcelWriter("swing_output.xlsx") as writer:
    breakout.to_excel(writer, sheet_name="Breakout", index=False)
    accumulation.to_excel(writer, sheet_name="Accumulation", index=False)

print("✅ Scanner Completed Successfully")
print("📁 Output File Created: swing_output.xlsx")
