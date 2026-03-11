from fastapi import FastAPI,Query
from pydantic import BaseModel,Field
from typing import Optional,List

app = FastAPI()

# Q1 - Add 3 More Products

@app.get("/")
def home():
    return {"message": "Welcome to my store API"}


# from fastapi import FastAPI

# app = FastAPI()

products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "price": 799,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": 2,
        "name": "Notebook",
        "price": 99,
        "category": "Stationery",
        "in_stock": True
    },
    {
        "id": 3,
        "name": "Pen Set",
        "price": 49,
        "category": "Stationery",
        "in_stock": False
    },
    {
        "id": 4,
        "name": "Water Bottle",
        "price": 299,
        "category": "Home",
        "in_stock": True
    },
    {
        "id": 5,
        "name": "Laptop Stand",
        "price": 1399,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": 6,
        "name": "Mechanical Keyboard",
        "price": 2599,
        "category": "Electronics",
        "in_stock": True
    },
    {
        "id": 7,
        "name": "Webcam HD",
        "price": 1799,
        "category": "Electronics",
        "in_stock": False
    }
]
feedback = []
orders = []

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
#Filter Products by Minimum Price
@app.get("/products/filter")
def filter_products(min_price: int = Query(None)):
    result = products
    if min_price:
        result = [p for p in products if p["price"] >= min_price]
    return {
        "filtered_products": result,
        "count": len(result)
    }

# Q2 - Category Filter Endpoint


@app.get("/products/category/{category_name}")
def filter_by_category(category_name: str):
    result = []

    for item in products:
        if item["category"].lower() == category_name.lower():
            result.append(item)

    if len(result) == 0:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }
    
#Get Only the Price of a Product
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return{
                "name":product["name"],
                "price": product["price"]
            }
    return {"error": "Product not found"}

# Q3 - Show Only In-Stock Products


@app.get("/products/instock")
def instock_products():
    available = []

    for item in products:
        if item["in_stock"]:
            available.append(item)

    return {
        "in_stock_products": available,
        "count": len(available)
    }



# Q4 - Store Summary

@app.get("/store/summary")
def store_summary():
    total = len(products)
    in_stock = 0
    categories = []

    for item in products:
        if item["in_stock"]:
            in_stock += 1

        if item["category"] not in categories:
            categories.append(item["category"])

    out_stock = total - in_stock

    return {
        "store_name": "Sai Laya Store",
        "total_products": total,
        "in_stock": in_stock,
        "out_of_stock": out_stock,
        "categories": categories
    }

#Build a Product Summary Dashboard
@app.get("/products/summary")
def product_summary():
    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]
    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])
    category = list(set(p["category"] for p in products))
    return{
        "total_products":len(products),
        "in_stock_cnt": len(in_stock),
        "out_stock_cnt": len(out_stock),
        "most_expensive": {
            "name":expensive["name"],
            "price":expensive["price"]
        },
        "cheapest":{
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": category
    }


# Q5 - Search Products

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    matches = []

    for item in products:
        if keyword.lower() in item["name"].lower():
            matches.append(item)

    if len(matches) == 0:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": matches,
        "total_matches": len(matches)
    }


# BONUS - Cheapest & Most Expensive

@app.get("/products/deals")
def deals():
    cheapest = products[0]
    expensive = products[0]

    for item in products:
        if item["price"] < cheapest["price"]:
            cheapest = item

        if item["price"] > expensive["price"]:
            expensive = item

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }
    
#Accept Customer Feedback
class CustomerFeedback(BaseModel):
    customer_name: str = Field(...,min_length=2,max_length=100)
    product_id: int =  Field(...,gt=0)
    rating: int = Field(...,ge=1,le=5)
    comment: Optional[str] = Field(None, max_length=300)
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())
    return{
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }

#Order Status Tracker
class Order(BaseModel):
    product_id: int
    quantity: int
@app.post("/orders")
def place_order(order:Order):
    for product in products:
        if product["id"] == order.product_id:
            if not product["in_stock"]:
                return {"error":"Product is out of stock"}
            new_order = {
                "order_id":len(orders)+1,
                "product":product["name"],
                "quantity":order.quantity,
                "total_price":product["price"] * order.quantity,
                "status":"pending"
            }
            orders.append(new_order)
            return{
                "message":"Order placed successfully",
                "order":new_order
            }
    return {"error": "Product not found"}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order
    return {"error": "Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return {
                "message": "Order confirmed",
                "order": order
            }
    return {"error": "Order not found"}

#Validate & Place a Bulk Order
class OrderItems(BaseModel):
    product_id: int = Field(...,gt=0)
    quantity: int= Field(...,gt=0, le=50)
class BulkOrder(BaseModel):
    company_name: str = Field(...,min_length=2)
    contact_email: str= Field(...,min_length=5)
    items: List[OrderItems]
    
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0
    for item in order.items:
    
        product = None
        for p in products:
            if p["id"] == item.product_id:
                product = p
                break
        if product is None:
            failed.append({
                "product_id" : item.product_id,
                "reason": "Product not found"
            })
        elif not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "quantity": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }
            