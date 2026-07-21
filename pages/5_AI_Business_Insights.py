import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL
from ai import generate_business_insights



st.set_page_config(

    page_title="AI Insights",

    page_icon="🤖",

    layout="wide"

)
with open("dashboard_style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )



engine=create_engine(
    DATABASE_URL
)



# -------------------------
# LOAD DATA
# -------------------------


orders=pd.read_sql(
    "SELECT * FROM orders",
    engine
)


products=pd.read_sql(
    "SELECT * FROM products",
    engine
)



customers=pd.read_sql(
    "SELECT * FROM customers",
    engine
)



order_items=pd.read_sql(
    "SELECT * FROM order_items",
    engine
)



# -------------------------
# METRICS
# -------------------------


revenue = orders[
    "net_amount"
].sum()



total_orders=len(
    orders
)



total_customers=len(
    customers
)



avg_order_value = (
    revenue /
    total_orders
    if total_orders
    else 0
)



low_stock=len(
    products[
        products.stock < 20
    ]
)



repeat_rate = (

    orders.customer_id
    .value_counts()
    .gt(1)
    .mean()

)



metrics={

"revenue":round(revenue,2),

"orders":total_orders,

"customers":total_customers,

"average_order_value":round(avg_order_value,2),

"low_stock":low_stock,

"repeat_customer_rate":
round(repeat_rate,2)

}




# -------------------------
# UI
# -------------------------


st.title(
"AI Buisness Insights"
)


st.markdown("""
### AI Executive Advisor

Generate an AI-powered executive report based on current business performance, customer behavior, inventory health, and revenue trends.
""")



if st.button(
"Generate AI Report"
):


    with st.spinner(
        "Analyzing business data..."
    ):


        report = generate_business_insights(
            metrics
        )
        print(report)


    st.success(
        "Analysis Completed"
    )


    st.markdown(
        report
    )



# -------------------------
# SHOW RAW METRICS
# -------------------------


c1, c2, c3 = st.columns(3)

c1.metric("Revenue", f"₹{revenue:,.0f}")
c2.metric("Orders", total_orders)
c3.metric("Customers", total_customers)

c4, c5, c6 = st.columns(3)

c4.metric("Average Order", f"₹{avg_order_value:,.0f}")
c5.metric("Low Stock", low_stock)
c6.metric("Repeat Customers", f"{repeat_rate:.0%}")

