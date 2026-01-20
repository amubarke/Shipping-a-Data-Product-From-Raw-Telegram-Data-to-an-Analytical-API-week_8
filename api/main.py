from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import get_db
from api import crud, schemas

app = FastAPI(
    title="Medical Analytics API",
    description="Analytical API exposing data warehouse insights",
    version="1.0"
)

# Endpoint 1
@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)


# Endpoint 2
@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    result = crud.get_channel_activity(db, channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result


# Endpoint 3
@app.get("/api/search/messages", response_model=List[schemas.MessageSearch])
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    return crud.search_messages(db, query, limit)


# Endpoint 4
@app.get("/api/reports/visual-content", response_model=List[schemas.VisualContentStats])
def visual_content(db: Session = Depends(get_db)):
    return crud.get_visual_content_stats(db)

@app.get("/")
def root():
    return {"message": "Medical Analytics API is running"}

