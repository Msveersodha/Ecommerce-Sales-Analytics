
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(
    page_title="E-Commerce Dashboard",
    layout="wide"
)

df = pd.read_csv("Cleaned_Superstore.csv")
model = joblib.load("best_model.pkl")

st.title("🛒 E-Commerce Sales Analytics Dashboard")

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

st.subheader("📌 KPI Cards")

c1,c2,c3 = st.columns(3)

c1.metric("Revenue", f"${filtered['Sales'].sum():,.0f}")

c2.metric("Profit", f"${filtered['Profit'].sum():,.0f}")

c3.metric("Orders", filtered["Order ID"].nunique())

st.subheader("📈 Monthly Sales")

monthly = filtered.groupby("Month Name")["Sales"].sum()

fig = px.line(
    monthly,
    x=monthly.index,
    y=monthly.values,
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Top Products")

top = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    top,
    x=top.values,
    y=top.index,
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📦 Category-wise Sales")

fig = px.pie(
    filtered,
    names="Category",
    values="Sales"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🌍 Regional Sales")

region_sales = filtered.groupby("Region")["Sales"].sum()

fig = px.bar(
    region_sales,
    x=region_sales.index,
    y=region_sales.values
)

st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard Developed Successfully!")
