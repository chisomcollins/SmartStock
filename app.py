import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SmartStock Lite", layout="wide")

st.title("📦 SmartStock Lite")
st.markdown("### AI Inventory Intelligence for Growing Retailers")
st.markdown("---")

# Upload option
uploaded_file = st.file_uploader("Upload Sales CSV (date, product, sales)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Custom dataset loaded successfully")
else:
    df = pd.read_csv("data/retail_sales_data.csv")
    st.info("Using demo dataset")

df['date'] = pd.to_datetime(df['date'])

product_list = df['product'].unique()
selected_product = st.selectbox("Select Product", product_list)

product_df = df[df['product'] == selected_product].sort_values("date")

# Forecast logic
last_30_days_avg = product_df.tail(30)['sales'].mean()
predicted_30_days = int(last_30_days_avg * 30)

current_stock = st.number_input("Current Stock Level", min_value=0, value=500)

reorder_quantity = max(0, predicted_30_days - current_stock)
stockout_ratio = predicted_30_days / (current_stock + 1)

# KPI SECTION
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("30-Day Demand Forecast", f"{predicted_30_days} units")
kpi2.metric("Current Stock", f"{current_stock} units")
kpi3.metric("Suggested Reorder", f"{reorder_quantity} units")

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("📊 Sales Trend")
    st.line_chart(product_df.set_index("date")["sales"])

with col2:
    st.subheader("📦 Risk Assessment")

    if stockout_ratio > 1:
        st.error("🔴 High Stockout Risk")
        st.write("Immediate reorder recommended.")
    elif stockout_ratio > 0.8:
        st.warning("🟡 Moderate Stockout Risk")
        st.write("Monitor closely and consider reorder.")
    else:
        st.success("🟢 Low Stockout Risk")
        st.write("Stock level healthy.")

st.markdown("---")
st.caption("SmartStock Lite • Built for SME inventory optimization")


