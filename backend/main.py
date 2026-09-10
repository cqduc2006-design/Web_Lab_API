import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/predict")
# Sử dụng def thay vì async def để dữ liệu trả về ngay lập tức
def predict_price(area: float, bedrooms: int, location: str = "others"):
    base_price = 500_000_000
    loc_mul = 1

    if location == "hcmc":
        loc_mul = 1.25
    elif location == "hanoi":
        loc_mul = 1.3

    
    predicted_price = round((base_price + (area * 15_000_000) + (bedrooms * 50_000_000)) * loc_mul)

    return {"area": area, "bedrooms": bedrooms, "location": location, "predicted_price": predicted_price}

