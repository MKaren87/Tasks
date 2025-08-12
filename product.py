from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List

app = FastAPI()

sample_products = [
    {"product_id": 123, "name": "Smartphone", "category": "Electronics", "price": 599.99},
    {"product_id": 456, "name": "Phone Case", "category": "Accessories", "price": 19.99},
    {"product_id": 789, "name": "Iphone", "category": "Electronics", "price": 1299.99},
    {"product_id": 101, "name": "Headphones", "category": "Accessories", "price": 99.99},
    {"product_id": 202, "name": "Smartwatch", "category": "Electronics", "price": 299.99}
]

@app.get("/products/search")
def search_products(
    keyword: str = Query(..., description="Ключевое слово для поиска"),
    category: Optional[str] = Query(None, description="Категория товара"),
    limit: int = Query(10, gt=0, description="Максимальное количество результатов")
) -> List[dict]:
    keyword_lower = keyword.lower()
    results = [
        product for product in sample_products
        if keyword_lower in product["name"].lower()
        and (category is None or product["category"].lower() == category.lower())
    ]
    return results[:limit]

@app.get("/product/{product_id}")
def get_product(product_id: int) -> dict:
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")