import asyncio
from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):  # what the client sends
    name: str
    price: float


class ItemPublic(BaseModel):  # what the client may see
    id: int
    name: str
    price: float


class ItemUpdate(BaseModel):
     name: str | None = None
     price: float | None = None


# PART D
class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int


# PART E
class HousePriceRequest(BaseModel):
    area_sqm: float = Field(gt = 0)
    bedrooms: int = Field(ge = 0)
    distance_to_center_km: float

_items: list[ItemPublic] = []
_next_id: int = 1

class HousePricePrediction(BaseModel):
    predicted_price: float
    currency: str = "VND"




def _find(item_id):
    for item in _items:
        if item.id ==  item_id:
            return item

    return None

# PART C
def _check_dup_name(new_name: str):
    for item in _items:
            if new_name.lower() == item.name.lower():
                raise HTTPException(status_code= 409, detail= "Item already exist")



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


#W7 Lab 
# GET ITEMS
@app.get("/items", response_model=list[ItemPublic])
def getItems():
    return _items

# GET ITEM BY ID
@app.get("/items/{item_id}")
def getItembyID(item_id: int):
    item = _find(item_id)

    if item == None:
        raise HTTPException(status_code = 404, detail = "Item not found")

    return item



# GET ITEM USING QUERY ------ PART B
@app.get("/items/query", response_model = ItemListResponse)
def getItemsbyQuery(skip: int = Query(0, ge = 0), 
                    limit: int = Query(10, ge = 1), 
                    min_price: float | None = None,
                    max_price: float | None = None,
                    q: str | None = Query(None, min_length = 2),
                    sort_by: str = Query("id", pattern="^(id|name|price)$"),
                    order: str = Query("asc", pattern="^(asc|desc)$") ):
    
    filtered_items = _items.copy()


    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]
        
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]
        
    if q is not None:
        filtered_items = [item for item in filtered_items if q.lower() in item.name.lower()]

    total = len(filtered_items)

    is_reverse = True if order == "desc" else False

    filtered_items.sort(key=lambda item: getattr(item, sort_by), reverse=is_reverse)

    return ItemListResponse(
        items=filtered_items[skip : skip + limit],
        total=total,
        skip=skip,
        limit=limit
    )



# CREATE ITEM
@app.post("/items", response_model=ItemPublic, status_code=201)
def createItem(data: ItemCreate):
    global _next_id

    _check_dup_name(data.name)
        
    item = ItemPublic(
        id = _next_id,
        name = data.name,
        price = data.price
    )

    _items.append(item)

    _next_id +=1

    return item


# UPDATE ITEM
@app.put("/items/{item_id}", response_model=ItemPublic)
def update(item_id: int, data: ItemCreate):
    item = _find(item_id)

    if item == None:
        raise HTTPException(status_code = 404, detail = "Item not found")

    index = _items.index(item)

    _check_dup_name(data.name)

    updated_item = ItemPublic(
        id = item.id,
        name = data.name,
        price = data.price
    )

    _items[index] = updated_item

    return updated_item


# PARTIAL UPDATE ------ PART A
@app.patch("/items/{item_id}", response_model = ItemPublic)
def partial_update(item_id: int, data: ItemUpdate):
    item = _find(item_id)
    if item == None:
        raise HTTPException(status_code = 404, detail = "Item not found")
     
    index = _items.index(item)
    if data.name is None:
        data.name = item.name
    elif data.name.lower() != item.name.lower():
        _check_dup_name(data.name)

    if data.price is None:
        data.price = item.price
     
    updated_item = ItemPublic(
        id = item.id,
        name = data.name,
        price = data.price
    )
     
    _items[index] = updated_item
     
    return updated_item

# DELETE ITEM BY ID
@app.delete("/items/{item_id}", status_code = 204)
def delete(item_id: int):
    item = _find(item_id)

    if item == None:
        raise HTTPException(status_code = 404, detail = "Item not found")

    _items.remove(item)

    return



# PART E
@app.post("/predict/house-price", response_model = HousePricePrediction)
def predict_house_price(data: HousePriceRequest):
    price = data.area_sqm * 15_000_000 - data.distance_to_center_km * 5_000_000 + data.bedrooms * 20_000_000

    return HousePricePrediction(
        predicted_price = price
    )


app.mount("/static", StaticFiles(directory="../frontend"), name="static")