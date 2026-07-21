import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from config import DATABASE_URL


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
    layout="wide"
)
with open("dashboard_style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )



# -----------------------------
# DATABASE CONNECTION
# -----------------------------

engine = create_engine(
    DATABASE_URL
)


# -----------------------------
# LOAD DATA
# -----------------------------

products = pd.read_sql(
    "SELECT * FROM products",
    engine
)

orders = pd.read_sql(
    "SELECT * FROM orders",
    engine
)

order_items = pd.read_sql(
    "SELECT * FROM order_items",
    engine
)


# -----------------------------
# PREPARE DATA
# -----------------------------

sales = (
    order_items
    .merge(
        products,
        on="product_id"
    )
)


sales["revenue"] = (
    sales["quantity"]
    *
    sales["unit_price"]
)


# -----------------------------
# TITLE
# -----------------------------

st.title(
    "Product Analytics Dashboard"
)


# -----------------------------
# KPI CALCULATION
# -----------------------------


total_products = len(products)

inventory_value = (
    products["price"]
    *
    products["stock"]
).sum()


total_units = (
    sales["quantity"]
    .sum()
)


out_of_stock = (
    products[
        products["stock"] <= 0
    ]
    .shape[0]
)


low_stock = (
    products[
        products["stock"] < 20
    ]
    .shape[0]
)



# -----------------------------
# KPI CARDS
# -----------------------------


c1,c2,c3,c4,c5 = st.columns(5)


c1.metric(
    "Products",
    total_products
)


c2.metric(
    "Inventory Value",
    f"₹{inventory_value:,.0f}"
)


c3.metric(
    "Units Sold",
    int(total_units)
)


c4.metric(
    "Low Stock",
    low_stock
)


c5.metric(
    "Out Of Stock",
    out_of_stock
)



# -----------------------------
# INVENTORY HEALTH
# -----------------------------


st.subheader(
    "Inventory Health"
)


inventory = products.copy()


inventory["status"] = (
    inventory["stock"]
    .apply(
        lambda x:
        "Out of Stock"
        if x <=0
        else
        "Low Stock"
        if x <20
        else
        "Healthy"
    )
)



fig = px.pie(
    inventory,
    names="status",
    title="Inventory Distribution"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -----------------------------
# CATEGORY PERFORMANCE
# -----------------------------


st.subheader(
    "Category Performance"
)


category = (
    sales
    .groupby("category")
    .agg(
        revenue=("revenue","sum"),
        units=("quantity","sum")
    )
    .reset_index()
)


fig = px.bar(
    category,
    x="category",
    y="revenue",
    title="Revenue By Category"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -----------------------------
# TOP PRODUCTS
# -----------------------------


st.subheader(
    "Fast Moving Products"
)



fast_products = (
    sales
    .groupby(
        [
            "product_id",
            "title"
        ]
    )
    .agg(
        units_sold=("quantity","sum"),
        revenue=("revenue","sum")
    )
    .sort_values(
        "units_sold",
        ascending=False
    )
    .head(20)
    .reset_index()
)



st.dataframe(
    fast_products,
    use_container_width=True
)



# -----------------------------
# SLOW PRODUCTS
# -----------------------------


st.subheader(
    "Slow Moving Products"
)



slow_products = (
    sales
    .groupby(
        [
            "product_id",
            "title"
        ]
    )
    .agg(
        units_sold=("quantity","sum")
    )
    .sort_values(
        "units_sold"
    )
    .head(20)
    .reset_index()
)



st.dataframe(
    slow_products,
    use_container_width=True
)



# -----------------------------
# STOCK VALUE ANALYSIS
# -----------------------------


st.subheader(
    "Inventory Value By Category"
)



stock_category = (
    products
    .assign(
        inventory_value=
        products["price"]
        *
        products["stock"]
    )
    .groupby("category")
    ["inventory_value"]
    .sum()
    .reset_index()
)



fig = px.treemap(
    stock_category,
    path=["category"],
    values="inventory_value",
    title="Capital Locked In Inventory"
)



st.plotly_chart(
    fig,
    use_container_width=True
)



# -----------------------------
# REORDER RECOMMENDATION
# -----------------------------


st.subheader(
    "Automated Reorder Recommendation"
)



recommendations = products[
    products["stock"] < 20
].copy()



recommendations["recommended_stock"] = (
    recommendations["stock"]
    +
    50
)



recommendations["action"] = (
    "Increase inventory"
)



if len(recommendations)>0:

    st.dataframe(
        recommendations[
            [
                "title",
                "stock",
                "recommended_stock",
                "action"
            ]
        ],
        use_container_width=True
    )

else:

    st.success(
        "All products have sufficient inventory"
    )



# -----------------------------
# EXPORT
# -----------------------------


csv = products.to_csv(
    index=False
)


st.download_button(
    "Download Product Report",
    csv,
    "product_report.csv",
    "text/csv"
)