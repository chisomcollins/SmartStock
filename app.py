import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartStock Lite", layout="wide")

st.title("📦 SmartStock Lite")
st.markdown("### AI Inventory Intelligence for Growing Retailers")
st.markdown("---")

#Onboarding
with st.expander("How to use SmartStock"):
    st.write("""
    1. Upload your sales CSV file.
    2. Select a product.
    3. Enter current stock level.
    4. Review demand forecast and reorder suggestion.
    """)
st.markdown("---")
  
# Downloadable sample
st.markdown("### 📥 Need a template?")
sample_data = pd.DataFrame({
    "date": ["2025-01-01", "2025-01-02"],
    "product": ["Rice 50kg", "Rice 50kg"],
    "sales": [45, 38]
})

csv_sample = sample_data.to_csv(index=False)

st.download_button(
    label="Download Sample CSV Template",
    data=csv_sample,
    file_name="smartstock_sample_template.csv",
    mime="text/csv"
)

st.markdown("---")

#Clear Data Format Instruction
st.info(
    "Your CSV must contain exactly these columns: "
    "`date`, `product`, `sales`. "
    "Date format should be YYYY-MM-DD."
)
# Upload option
uploaded_file = st.file_uploader(
    "Upload Sales CSV (must contain: date, product, sales)", 
    type=["csv"]
)

# Load dataset
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Custom dataset loaded successfully")
else:
    try:
        df = pd.read_csv("data/retail_sales_data.csv")
        st.info("Using demo dataset")
    except:
        st.error("Demo dataset not found. Please upload a CSV file.")
        st.stop()

# Validate required columns
required_columns = {"date", "product", "sales"}

if not required_columns.issubset(df.columns):
    st.error("CSV must contain columns: date, product, sales")
    st.write("Current columns found:", df.columns.tolist())
    st.stop()

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Product selection
product_list = df["product"].unique()
selected_product = st.selectbox("Select Product", product_list)

# Filter product data
product_df = df[df["product"] == selected_product].sort_values("date")

if product_df.empty:
    st.warning("No data available for selected product.")
    st.stop()

# Forecast logic
# Forecast
last_30_days_avg = product_df.tail(30)["sales"].mean()
predicted_30_days = int(last_30_days_avg * 30)

# Stock Input
current_stock = st.number_input("Current Stock Level", min_value=0, value=500)

# Reorder logic
reorder_quantity = max(0, predicted_30_days - current_stock)


# --- Normalized Structured Risk Framework ---

# Demand Pressure
raw_pressure = predicted_30_days / (current_stock + 1)
pressure_score = min(1, raw_pressure / 2)

# Volatility
volatility = product_df.tail(30)["sales"].std() or 0
mean_sales = product_df["sales"].mean()
raw_volatility = volatility / (mean_sales + 1)
volatility_score = min(1, raw_volatility)

# Lead Time Exposure
daily_avg_sales = mean_sales
days_until_stockout = current_stock / (daily_avg_sales + 1)

supplier_lead_time = st.number_input(
    "Supplier Lead Time (days)", 
    min_value=0, 
    value=7
)

raw_lead_exposure = supplier_lead_time / (days_until_stockout + 1)
lead_time_score = min(1, raw_lead_exposure)

# Weighted Risk Score
risk_score = int(
    (pressure_score * 50) +
    (volatility_score * 30) +
    (lead_time_score * 20)
)


# KPI Section
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("30-Day Demand Forecast", f"{predicted_30_days} units")
kpi2.metric("Current Stock", f"{current_stock} units")
kpi3.metric("Suggested Reorder", f"{reorder_quantity} units")

# Risk Score display
st.markdown("### 📉 Stockout Risk Score")
st.progress(risk_score / 100)
st.write(f"Risk Score: **{risk_score}/100**")

st.markdown("### 🚚 Reorder Timing Intelligence")
if days_until_stockout <= supplier_lead_time:
    st.error(
        f"You may stock out in approximately {int(days_until_stockout)} days. "
        f"Reorder immediately to avoid disruption."
    )
else:
    safe_window = int(days_until_stockout - supplier_lead_time)
    st.success(
        f"You have approximately {safe_window} days before reorder becomes urgent."
    )


if volatility_score > 0.6:
    st.warning("⚠️ High demand volatility detected.")
elif volatility_score > 0.3:
    st.info("Moderate demand variability.")
else:
    st.success("Stable demand pattern.")

st.markdown("---")


col1, col2 = st.columns([2,1])

with col1:
    st.subheader("📊 Sales Trend")
    st.line_chart(product_df.set_index("date")["sales"])

with col2:
    st.subheader("📦 Risk Assessment")

    if risk_score >= 66:
        st.error("🔴 High Stockout Risk")
        st.write("Strong likelihood of stockout without intervention.")
    elif risk_score >= 36:
        st.warning("🟡 Moderate Stockout Risk")
        st.write("Monitor demand closely and prepare reorder plan.")
    else:
        st.success("🟢 Low Stockout Risk")
        st.write("Inventory position is currently stable.")
         

# Summary part
st.markdown("### 📊 Business Summary")

if reorder_quantity > 0:
    st.write(
        f"If sales continue at current pace, you may need to reorder "
        f"approximately **{reorder_quantity} units** within the next 30 days."
    )
else:
    st.write(
        "Your current inventory level appears sufficient for projected demand."
    )


st.markdown("---")
st.caption("SmartStock Lite • Built for SME inventory optimization")
