import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Page Config
st.set_page_config(page_title="Database Dashboard", layout="wide")

st.title("📊 Database Visualization Dashboard")

# Database Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="engineering_db"   # Change to your DB name
    )

    query = "SELECT * FROM applications"  # Change table name
    df = pd.read_sql(query, conn)

    st.success("Database Connected Successfully!")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# Display Data
st.subheader("Dataset Preview")
st.dataframe(df)

# Dataset Information
st.subheader("Dataset Information")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

# Select Columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

if len(numeric_cols) > 0:

    st.subheader("Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Histogram", "Pie Chart"]
    )

    col1 = st.selectbox("X-Axis", df.columns)

    if chart_type != "Pie Chart":
        col2 = st.selectbox("Y-Axis", numeric_cols)

    # Bar Chart
    if chart_type == "Bar Chart":
        fig = px.bar(df, x=col1, y=col2)
        st.plotly_chart(fig, use_container_width=True)

    # Line Chart
    elif chart_type == "Line Chart":
        fig = px.line(df, x=col1, y=col2)
        st.plotly_chart(fig, use_container_width=True)

    # Histogram
    elif chart_type == "Histogram":
        fig = px.histogram(df, x=col2)
        st.plotly_chart(fig, use_container_width=True)

    # Pie Chart
    elif chart_type == "Pie Chart":
        value_col = st.selectbox("Values", numeric_cols)
        fig = px.pie(df, names=col1, values=value_col)
        st.plotly_chart(fig, use_container_width=True)

# Correlation Heatmap
if len(numeric_cols) > 1:
    st.subheader("Correlation Matrix")

    corr = df[numeric_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)

# Download Dataset
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Data",
    csv,
    "dataset.csv",
    "text/csv"
)