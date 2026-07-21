import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import create_engine

from prophet import Prophet

from config import DATABASE_URL



# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(

    page_title="Forecasting",

    page_icon="📉",

    layout="wide"

)
with open("dashboard_style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# -----------------------------
# DATABASE
# -----------------------------


engine = create_engine(
    DATABASE_URL
)



orders = pd.read_sql(

    "SELECT * FROM orders",

    engine

)



orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)



# -----------------------------
# TITLE
# -----------------------------


st.title(
    "Ecommerce Forecasting Dashboard"
)


st.caption(
    "AI powered revenue and demand prediction"
)



# -----------------------------
# PREPARE DATA
# -----------------------------


daily_sales = (

orders

.groupby(

orders.order_date.dt.date

)

["net_amount"]

.sum()

.reset_index()

)



daily_sales.columns=[

"ds",

"y"

]


daily_sales["ds"] = pd.to_datetime(

daily_sales["ds"]

)



# -----------------------------
# HISTORICAL TREND
# -----------------------------


st.subheader(

"Historical Revenue"

)



fig = px.line(

daily_sales,

x="ds",

y="y",

markers=True

)



st.plotly_chart(

fig,

use_container_width=True

)



# -----------------------------
# FORECAST MODEL
# -----------------------------


days = st.slider(

"Forecast Days",

7,

90,

30

)



if len(daily_sales) >= 10:


    model = Prophet()


    model.fit(
        daily_sales
    )


    future = model.make_future_dataframe(

        periods=days

    )


    forecast = model.predict(

        future

    )



    st.subheader(

    "Future Revenue Prediction"

    )


    fig = px.line(

        forecast,

        x="ds",

        y=[

            "yhat",

            "yhat_lower",

            "yhat_upper"

        ],

        title="Revenue Forecast"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )



    # -----------------------------
    # FORECAST TABLE
    # -----------------------------


    st.subheader(

    "Predicted Revenue"

    )


    prediction=(

    forecast

    [

        [

        "ds",

        "yhat"

        ]

    ]

    .tail(days)

    )


    st.dataframe(

        prediction,

        use_container_width=True

    )



    # -----------------------------
    # BUSINESS INSIGHTS
    # -----------------------------


    total_prediction = (

        prediction["yhat"]

        .sum()

    )


    st.metric(

        "Expected Revenue Next Period",

        f"₹{total_prediction:,.0f}"

    )



else:


    st.warning(

    "Need more historical data for forecasting. Generate more orders."

    )