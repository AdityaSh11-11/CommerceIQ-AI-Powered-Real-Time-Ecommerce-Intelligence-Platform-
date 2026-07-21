import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine
from datetime import datetime

from config import DATABASE_URL

from streamlit_autorefresh import st_autorefresh



# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(

    page_title="Live Order Monitor",

    page_icon="⚡",

    layout="wide"

)

with open("dashboard_style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )



# -------------------------
# AUTO REFRESH
# -------------------------
st_autorefresh(
    interval=3000,
    key="order_refresh"
)



# -------------------------
# DATABASE
# -------------------------

engine = create_engine(
    DATABASE_URL
)



# -------------------------
# LOAD ORDERS
# -------------------------

@st.cache_data(ttl=2)
def load_orders():

    return pd.read_sql(
        """
        SELECT *
        FROM orders
        ORDER BY order_date DESC
        """,
        engine
    )


orders = load_orders()



orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)



# -------------------------
# TITLE
# -------------------------

st.title(
    "Live Order Monitor Dashboard"
)



st.caption(
    "Real-time monitoring system"
)



# -------------------------
# METRICS
# -------------------------


total_orders = len(
    orders
)


revenue = orders[
    "net_amount"
].sum()



today_orders = orders[
    orders.order_date.dt.date
    ==
    datetime.now().date()
]



orders_per_minute = (
    len(today_orders)
    /
    max(
        datetime.now().hour*60+
        datetime.now().minute,
        1
    )
)



c1,c2,c3,c4 = st.columns(4)



c1.metric(

    "Total Orders",

    total_orders

)


c2.metric(

    "Revenue",

    f"₹{revenue:,.0f}"

)


c3.metric(

    "Today's Orders",

    len(today_orders)

)


c4.metric(

    "Orders / Minute",

    round(
        orders_per_minute,
        2
    )

)



# -------------------------
# ORDER STATUS
# -------------------------

st.subheader(
    "Order Status Monitor"
)



status = (

orders["status"]

.value_counts()

.reset_index()

)



status.columns=[

"Status",

"Count"

]



fig = px.bar(

    status,

    x="Status",

    y="Count",

    title="Live Order Status"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# -------------------------
# LIVE REVENUE TREND
# -------------------------


st.subheader(

"Transaction Velocity"

)



minute_sales=(

orders

.groupby(

orders.order_date.dt.hour

)

["net_amount"]

.sum()

.reset_index()

)



minute_sales.columns=[

"Hour",

"Revenue"

]



fig = px.line(

minute_sales,

x="Hour",

y="Revenue",

markers=True,

title="Hourly Revenue Flow"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# -------------------------
# RECENT ORDERS
# -------------------------


st.subheader(

"Incoming Orders"

)



recent = (

orders

.sort_values(

"order_date",

ascending=False

)

.head(25)

)



st.dataframe(

recent,

use_container_width=True

)



# -------------------------
# ALERT SYSTEM
# -------------------------


st.subheader(

"Automated Alerts"

)



if orders_per_minute > 5:


    st.success(

        "High order velocity detected"

    )


else:


    st.info(

        "Order activity is normal"

    )



cancelled = len(

orders[
orders.status=="Cancelled"
]

)



if cancelled > total_orders*0.1:


    st.warning(

        "Cancellation rate is high"

    )