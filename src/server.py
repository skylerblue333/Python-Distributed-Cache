from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .cache import LRUCache
import uvicorn

app = FastAPI(title="Distributed Cache Node")
cache = LRUCache(capacity=10000, ttl=300)

class CacheItem(BaseModel):
    key: str
    value: str

@app.get("/cache/{key}")
def get_item(key: str):
    val = cache.get(key)
    if val is None:
        raise HTTPException(status_code=404, detail="Key not found or expired")
    return {"key": key, "value": val}

@app.post("/cache")
def set_item(item: CacheItem):
    cache.set(item.key, item.value)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
