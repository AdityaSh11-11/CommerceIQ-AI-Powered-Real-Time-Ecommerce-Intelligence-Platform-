import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from database import engine
from config import DATABASE_URL

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
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
customers = pd.read_sql("SELECT * FROM customers", engine)
order_items = pd.read_sql("SELECT * FROM order_items", engine)

orders["order_date"] = pd.to_datetime(orders["order_date"])

revenue = orders["net_amount"].sum()

orders_count = len(orders)

customers_count = len(customers)

aov = revenue / orders_count if orders_count else 0

products_sold = order_items["quantity"].sum()

profit = (
    orders["net_amount"].sum()
    - orders["tax"].sum()
)

st.title("Executive Dashboard")

c1, c2, c3 = st.columns(3)

c4, c5, c6 = st.columns(3)

c1.metric("Revenue", f"₹{revenue:,.0f}")

c2.metric("Orders", orders_count)

c3.metric("Customers", customers_count)

c4.metric("Average Order", f"₹{aov:,.0f}")

c5.metric("Products Sold", products_sold)

c6.metric("Estimated Profit", f"₹{profit:,.0f}")

daily = (
    orders.groupby(
        orders["order_date"].dt.date
    )["net_amount"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily,
    x="order_date",
    y="net_amount",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

sales = order_items.merge(
    products,
    on="product_id"
)

top = (
    sales.groupby("title")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top,
    x="title",
    y="quantity",
    title="Top Selling Products"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

sales["sales"] = (
    sales["quantity"] *
    sales["unit_price"]
)

category = (
    sales.groupby("category")["sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    category,
    values="sales",
    names="category",
    title="Category Contribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Latest Orders")

st.dataframe(
    orders.sort_values(
        "order_date",
        ascending=False
    ).head(20),
    use_container_width=True
)

st.subheader("Inventory Alert")

low = products[
    products["stock"] < 20
]

st.dataframe(
    low[
        [
            "title",
            "stock",
            "category"
        ]
    ],
    use_container_width=True
)