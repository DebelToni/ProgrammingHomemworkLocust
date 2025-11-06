"""Sample FastAPI application with multiple endpoints for load-testing demos."""

from __future__ import annotations

from datetime import datetime
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Programming Homework Locust API", version="1.0.0")


class Item(BaseModel):
    id: int
    name: str
    price: float
    stock: int


class OrderRequest(BaseModel):
    item_id: int
    quantity: int


class OrderResponse(BaseModel):
    total_price: float
    message: str
    remaining_stock: int


# Seed data keeps things simple for demos; no persistence required.
inventory: Dict[int, Item] = {
    1: Item(id=1, name="Red Potion", price=9.99, stock=120),
    2: Item(id=2, name="Blue Potion", price=12.5, stock=80),
    3: Item(id=3, name="Magic Scroll", price=29.0, stock=45),
}


@app.get("/health")
async def health_check() -> dict:
    """Return service health along with a timestamp."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/items")
async def list_items() -> dict:
    """List all available items."""
    return {"items": list(inventory.values())}


@app.get("/items/{item_id}")
async def get_item(item_id: int) -> Item:
    """Return a single item by id."""
    try:
        return inventory[item_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Item not found") from exc


@app.post("/orders", response_model=OrderResponse)
async def create_order(request: OrderRequest) -> OrderResponse:
    """Create an order if sufficient stock is available."""
    item = inventory.get(request.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if request.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    if request.quantity > item.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Requested {request.quantity}, but only {item.stock} remaining.",
        )

    item.stock -= request.quantity
    total_price = round(item.price * request.quantity, 2)

    return OrderResponse(
        total_price=total_price,
        message=f"Order placed for {request.quantity}x {item.name}",
        remaining_stock=item.stock,
    )


@app.get("/orders/estimate/{item_id}")
async def estimate_order(item_id: int, quantity: int = 1) -> dict:
    """Return a pricing estimate without reducing stock."""
    item = inventory.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    estimated_price = round(item.price * quantity, 2)

    return {
        "item_id": item_id,
        "quantity": quantity,
        "estimated_price": estimated_price,
        "in_stock": item.stock,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
