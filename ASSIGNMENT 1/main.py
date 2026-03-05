from fastapi import FastAPI

app = FastAPI()

# Q1 - Add 3 More Products

@app.get("/")
def home():
    return {"message": "Welcome to my store API"}


from fastapi import FastAPI

app = FastAPI()

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

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
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