import pandas as pd

print("📊 Professional NSE Swing Scanner Running...\n")

# Load bhavcopy file
file_name = "sec_bhavdata_full_13022026.csv"
df = pd.read_csv(file_name)

# Clean column names
df.columns = df.columns.str.strip()

# Keep only EQ series
df = df[df["SERIES"] == "EQ"]

# Convert required columns
numeric_cols = [
    "OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE",
    "CLOSE_PRICE", "TTL_TRD_QNTY",
    "DELIV_QTY", "DELIV_PER",
    "TURNOVER_LACS"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with missing data
df = df.dropna()

# Liquidity Filter (avoid junk stocks)
df = df[df["TURNOVER_LACS"] > 500]

# Close Strength (close near high)
df["Close_Strength"] = (
    (df["CLOSE_PRICE"] - df["LOW_PRICE"]) /
    (df["HIGH_PRICE"] - df["LOW_PRICE"] + 0.0001)
)

# 🔥 Breakout Candidates
breakout = df[
    (df["Close_Strength"] > 0.7) &
    (df["DELIV_PER"] > 45)
].copy()

breakout["Score"] = (
    breakout["DELIV_PER"] * 0.6 +
    breakout["Close_Strength"] * 40
)

breakout = breakout.sort_values("Score", ascending=False)

# 🏗 Accumulation Candidates
accumulation = df[
    (df["DELIV_PER"] > 60) &
    (df["Close_Strength"] > 0.5)
].copy()

accumulation = accumulation.sort_values("DELIV_PER", ascending=False)

# Save output
with pd.ExcelWriter("swing_output.xlsx") as writer:
    breakout.to_excel(writer, sheet_name="Breakout", index=False)
    accumulation.to_excel(writer, sheet_name="Accumulation", index=False)

print("✅ Scanner Completed Successfully")
print("📁 Output File Created: swing_output.xlsx")
