from sqlalchemy.orm import Session

from database import engine
from models import Order, OrderItem

session = Session(engine)

print("=" * 50)

print("Orders      :", session.query(Order).count())

print("Order Items :", session.query(OrderItem).count())

print("=" * 50)

latest = session.query(Order).order_by(Order.order_id.desc()).first()

print("Latest Order")

if latest is None:
    print("No orders found.")
else:
    print(latest.order_id)
    print(latest.total_amount)
    print(latest.status)

session.close()