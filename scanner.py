import pandas as pd
import os

print("Current working directory:", os.getcwd())

# ---------- LOAD BHAVCOPY ----------
df = pd.read_csv("data/bhavcopy.csv")

print("Rows Loaded:", len(df))

# ---------- CLEAN COLUMN NAMES ----------
df.columns = df.columns.str.strip().str.upper()

# ---------- ENSURE REQUIRED COLUMNS ----------
required_cols = ["SYMBOL", "CLOSE", "PCT_CHANGE", "DELIV_PER", "TTL_TRD_QNTY"]

for col in required_cols:
    if col not in df.columns:
        print(f"Missing column: {col}")
        exit()

# ---------- CONVERT TO NUMERIC ----------
df["PCT_CHANGE"] = pd.to_numeric(df["PCT_CHANGE"], errors="coerce")
df["DELIV_PER"] = pd.to_numeric(df["DELIV_PER"], errors="coerce")
df["TTL_TRD_QNTY"] = pd.to_numeric(df["TTL_TRD_QNTY"], errors="coerce")

df = df.dropna()

# ---------- MOMENTUM SCORE ----------
df["MOMENTUM_SCORE"] = (
    df["PCT_CHANGE"] * 100 +
    df["TTL_TRD_QNTY"] / 100000
)

# ---------- ACCUMULATION SCORE ----------
df["ACCUMULATION_SCORE"] = (
    df["DELIV_PER"] * 10 +
    df["TTL_TRD_QNTY"] / 200000
)

# ---------- FINAL SCORE ----------
df["FINAL_SCORE"] = df["MOMENTUM_SCORE"] + df["ACCUMULATION_SCORE"]

# ---------- SORT ----------
df = df.sort_values("FINAL_SCORE", ascending=False)

# ---------- KEEP TOP 20 ----------
df = df.head(20)

# ---------- SAVE OUTPUT ----------
output_path = os.path.join(os.getcwd(), "swing_output.xlsx")

df.to_excel(output_path, index=False)

print("File saved at:", output_path)
print("Done Successfully.")
