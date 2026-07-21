import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from config import DATABASE_URL

st.set_page_config(
    page_title="Sales Analytics",
    layout="wide"
)
with open("dashboard_style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
engine = create_engine(DATABASE_URL)

orders = pd.read_sql("SELECT * FROM orders", engine)

products = pd.read_sql("SELECT * FROM products", engine)

order_items = pd.read_sql("SELECT * FROM order_items", engine)

customers = pd.read_sql("SELECT * FROM customers", engine)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

sales = (
    order_items
    .merge(products, on="product_id")
    .merge(orders, on="order_id")
)

sales["Revenue"] = (
    sales["quantity"] *
    sales["unit_price"]
)

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(sales["category"].unique()),
    default=sorted(sales["category"].unique())
)

brand = st.sidebar.multiselect(
    "Brand",
    sorted(sales["brand"].unique()),
    default=sorted(sales["brand"].unique())
)

sales = sales[
    sales["category"].isin(category)
]

sales = sales[
    sales["brand"].isin(brand)
]
st.title(
    "Sales Analytics Dashboard"
)
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Revenue",
    f"₹{sales['Revenue'].sum():,.0f}"
)

c2.metric(
    "Products Sold",
    int(sales["quantity"].sum())
)

c3.metric(
    "Categories",
    sales["category"].nunique()
)

c4.metric(
    "Brands",
    sales["brand"].nunique()
)

category_sales = (
    sales.groupby("category")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="category",
    y="Revenue",
    title="Revenue by Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

brand_sales = (
    sales.groupby("brand")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.treemap(
    brand_sales,
    path=["brand"],
    values="Revenue",
    title="Brand Contribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

top = (
    sales.groupby("title")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("Top Products")

st.dataframe(top)

bottom = (
    sales.groupby("title")["Revenue"]
    .sum()
    .sort_values()
    .head(10)
)

st.subheader("Bottom Products")

st.dataframe(bottom)

sales["Month"] = sales["order_date"].dt.to_period("M").astype(str)

monthly = (
    sales.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

csv = sales.to_csv(index=False)

st.download_button(
    "Download Sales Data",
    csv,
    "sales.csv",
    "text/csv"
)