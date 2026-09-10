import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/predict")
# We use a synchronous `def` instead of `async def` because this endpoint performs simple task, no need for async here.
def predict_price(area: float, bedrooms: int, location: str = "others"):
    base_price = 500_000_000
    loc_mul = 1

    if location == "hcmc":
        loc_mul = 1.25
    elif location == "hanoi":
        loc_mul = 1.3

    
    predicted_price = round((base_price + (area * 15_000_000) + (bedrooms * 50_000_000)) * loc_mul)

    return {"area": area, "bedrooms": bedrooms, "location": location, "predicted_price": predicted_price}

app.mount("/static", StaticFiles(directory="../frontend"), name="static")