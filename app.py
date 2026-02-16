import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SmartStock", layout="wide")

st.title("📦 SmartStock Lite")
st.markdown("### Inventory Intelligence for Small Retailers")

# Load dataset
df = pd.read_csv("data/retail_sales_data.csv")
df['date'] = pd.to_datetime(df['date'])

product_list = df['product'].unique()
selected_product = st.selectbox("Select Product", product_list)

product_df = df[df['product'] == selected_product].sort_values("date")

# Forecast logic (simple moving average)
last_30_days_avg = product_df.tail(30)['sales'].mean()
predicted_30_days = int(last_30_days_avg * 30)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sales Trend")
    st.line_chart(product_df.set_index("date")["sales"])

with col2:
    st.subheader("📦 Inventory Decision Panel")

    current_stock = st.number_input("Current Stock Level", min_value=0, value=500)

    st.metric("Predicted 30-Day Demand", f"{predicted_30_days} units")

    reorder_quantity = max(0, predicted_30_days - current_stock)

    st.markdown("---")

    if reorder_quantity > 0:
        st.error(f"⚠ You may run out of stock.")
        st.markdown(f"### Suggested Reorder: **{reorder_quantity} units**")
    else:
        st.success("✅ Current stock level is sufficient.")

    stockout_ratio = predicted_30_days / (current_stock + 1)

    if stockout_ratio > 1:
        st.error("🔴 High Stockout Risk")
    elif stockout_ratio > 0.8:
        st.warning("🟡 Moderate Stockout Risk")
    else:
        st.success("🟢 Low Stockout Risk")

st.markdown("---")
st.caption("SmartStock Lite • AI-powered inventory forecasting prototype")
