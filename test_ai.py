from ai import generate_business_insights


data = {

"revenue":500000,

"orders":1200,

"average_order_value":416,

"low_stock":15

}


print(
    generate_business_insights(data)
)