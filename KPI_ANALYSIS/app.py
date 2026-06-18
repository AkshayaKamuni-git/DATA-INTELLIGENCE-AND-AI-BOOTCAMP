import streamlit as st
import pandas as pd
import plotly.express as px

# Page Title
st.set_page_config(page_title="Sales KPI Dashboard", layout="wide")

st.title("📊 Sales KPI Analysis Dashboard")

# Sample Sales Dataset
data = {
    "Product": ["Laptop", "Mobile", "Tablet", "Laptop", "Mobile", "Tablet"],
    "Region": ["North", "South", "East", "West", "North", "South"],
    "Sales": [50000, 30000, 20000, 45000, 35000, 25000],
    "Quantity": [10, 15, 8, 9, 18, 12]
}

df = pd.DataFrame(data)

# Display Dataset
st.subheader("Sales Dataset")
st.dataframe(df)

# KPI Calculations
total_sales = df["Sales"].sum()
total_quantity = df["Quantity"].sum()
average_sales = df["Sales"].mean()

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Sales", f"₹{total_sales:,}")

with col2:
    st.metric("📦 Total Quantity", total_quantity)

with col3:
    st.metric("📈 Average Sales", f"₹{average_sales:,.2f}")

# Sales by Product
st.subheader("Sales by Product")
product_sales = df.groupby("Product")["Sales"].sum().reset_index()

fig1 = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    color="Product",
    title="Sales by Product"
)

st.plotly_chart(fig1, use_container_width=True)

# Sales by Region
st.subheader("Sales by Region")
region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig2 = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    title="Regional Sales Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# Top Product
top_product = product_sales.loc[
    product_sales["Sales"].idxmax(), "Product"
]

st.success(f"🏆 Best Selling Product: {top_product}")