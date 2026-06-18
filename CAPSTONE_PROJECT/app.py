import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Sales Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce.csv")

    # Convert date safely
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

state = st.sidebar.multiselect(
    "State",
    options=df["State"].unique(),
    default=df["State"].unique()
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["State"].isin(state))
]

# KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Orders", total_orders)
c4.metric("Quantity", total_quantity)

st.divider()

# Monthly Sales
filtered_df["Month"] = (
    filtered_df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# Category Sales
col1, col2 = st.columns(2)

with col1:
    cat_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        cat_sales,
        x="Category",
        y="Sales",
        title="Category Sales",
        color="Category"
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.pie(
        cat_sales,
        names="Category",
        values="Sales",
        title="Sales Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Top Products
top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top Products"
)

st.plotly_chart(fig4, use_container_width=True)

# State Sales
state_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    state_sales,
    x="State",
    y="Sales",
    color="Sales",
    title="State-wise Sales"
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("Dataset")

st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)