from typing import List, Annotated
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

origins = [
  "http://localhost",
  "http://localhost:8080",
  "http://127.0.0.1:8000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class RatingBase(BaseModel):
  star: float

def get_db():
  db = SessionLocal()

  try:
    yield db
  finally:
    db.close()


db_dependency = Annotated[Session, Depends(get_db)]
  
@app.get("/ratings/")
async def get_all_ratings(db: db_dependency):
  ratings_query = db.query(models.Ratings).all()
  return ratings_query

@app.post("/ratings/")
async def create_ratings(rating: RatingBase, db: db_dependency):
  db_rating = models.Ratings(star = rating.star)
  db.add(db_rating)
  db.commit()
  db.refresh(db_rating)

