import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from config import DATABASE_URL

st.set_page_config(
    page_title="Customer Analytics",
    layout="wide"
)
with open("dashboard_style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

engine = create_engine(DATABASE_URL)

orders = pd.read_sql("SELECT * FROM orders", engine)

customers = pd.read_sql("SELECT * FROM customers", engine)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

customer_sales = (
    orders.merge(
        customers,
        on="customer_id"
    )
)

total_customers = len(customers)

active_customers = customer_sales["customer_id"].nunique()

repeat_customers = (
    customer_sales
    .groupby("customer_id")
    .size()
    .gt(1)
    .sum()
)

avg_customer_value = (
    customer_sales["net_amount"].sum()
    / active_customers
)
st.title(
    "Customer Analytics Dashboard"
)
c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Customers",
    total_customers
)

c2.metric(
    "Active",
    active_customers
)

c3.metric(
    "Repeat",
    repeat_customers
)

c4.metric(
    "Customer Value",
    f"₹{avg_customer_value:,.0f}"
)

city = (
    customer_sales
    .groupby("city")["net_amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    city,
    x="city",
    y="net_amount",
    title="Revenue by City"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

country = (
    customer_sales
    .groupby("country")["net_amount"]
    .sum()
    .reset_index()
)

fig = px.pie(
    country,
    values="net_amount",
    names="country",
    title="Revenue by Country"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

top = (
    customer_sales
    .groupby(
        [
            "customer_id",
            "first_name",
            "last_name"
        ]
    )["net_amount"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(15)
)

st.subheader(
    "Top Customers"
)

st.dataframe(
    top,
    use_container_width=True
)

customer_value = (
    customer_sales
    .groupby("customer_id")["net_amount"]
    .sum()
)

segments = pd.cut(

    customer_value,

    bins=[0,1000,5000,100000],

    labels=[
        "Low Value",
        "Medium Value",
        "High Value"
    ]

)

segment = (
    segments
    .value_counts()
    .reset_index()
)

segment.columns=[
    "Segment",
    "Customers"
]

fig = px.pie(

    segment,

    values="Customers",

    names="Segment",

    title="Customer Segments"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

clv = (
    customer_sales
    .groupby("customer_id")["net_amount"]
    .mean()
    .reset_index()
)

fig = px.histogram(

    clv,

    x="net_amount",

    nbins=30,

    title="Customer Lifetime Value"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader(
    "Customer Data"
)

st.dataframe(
    customer_sales,
    use_container_width=True
)