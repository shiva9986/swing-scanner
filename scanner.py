import streamlit as st
import pandas as pd

st.title("📊 Professional NSE Swing Scanner")

uploaded_file = st.file_uploader("Upload NSE Full Bhavcopy CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Columns detected:", df.columns)

    # Keep only EQ series
    df = df[df["SERIES"] == "EQ"]

    # Convert numeric columns
    numeric_cols = ["CLOSE_PRICE", "TOTTRDQTY", "DELIV_PER"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filters
    volume_filter = df["TOTTRDQTY"] > df["TOTTRDQTY"].mean()
    delivery_filter = df["DELIV_PER"] > 40
    price_filter = df["CLOSE_PRICE"] > 100

    scanner = df[volume_filter & delivery_filter & price_filter]

    st.subheader("🔥 Swing Candidates")
    st.dataframe(scanner.sort_values("TOTTRDQTY", ascending=False))

else:
    st.info("Upload bhavcopy file to start scanning")
