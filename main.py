from http.client import HTTPException
from urllib.request import Request
from fastapi import FastAPI
from fastapi import Depends, status
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.database import get_db
from models.models import recipe
from models.pydantic.recipe import RecipeCreate, RecipeUpdate

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

'''
{
  "message": "Recipe details by id",
  "recipe": [
    {
      "id": 1,
      "title": "チキンカレー",
      "making_time": "45分",
      "serves": "4人",
      "ingredients": "玉ねぎ,肉,スパイス",
      "cost": "1000"
    }
  ]
}
'''
@app.get('/recipes/{recipe_id}')
def get_recipe(recipe_id: str, db: Session = Depends(get_db)):
    result = db.query(recipe).filter(recipe.id==recipe_id).all()
    return {
        "message": "Recipe details by id",
        "recipe": result
    }

'''
  {
    "recipes": [
      {
        "id": 1,
        "title": "チキンカレー",
        "making_time": "45分",
        "serves": "4人",
        "ingredients": "玉ねぎ,肉,スパイス",
        "cost": "1000"
      },
      {
        "id": 2,
        "title": "オムライス",
        "making_time": "30分",
        "serves": "2人",
        "ingredients": "玉ねぎ,卵,スパイス,醤油",
        "cost": "700"
      },
      {
        "id": 3,
        "title": "トマトスープ",
        "making_time": "15分",
        "serves": "5人",
        "ingredients": "玉ねぎ, トマト, スパイス, 水",
        "cost": "450"
      }
    ]
  }
'''
@app.get('/recipes')
def get_recipe_all(db: Session = Depends(get_db)):
    results = db.query(recipe).all()
    return {
        "recipes": results
    }

'''
{
  "message": "Recipe successfully created!",
  "recipe": [
    {
      "id": 3,
      "title": "トマトスープ",
      "making_time": "15分",
      "serves": "5人",
      "ingredients": "玉ねぎ, トマト, スパイス, 水",
      "cost": "450",
      "created_at": "2016-01-12 14:10:12",
      "updated_at": "2016-01-12 14:10:12"
    }
  ]
}
OR
{
 "message": "Recipe creation failed!",
 "required": "title, making_time, serves, ingredients, cost"
}
'''
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    return {
        "message": "Recipe creation failed!",
        "required": "title, making_time, serves, ingredients, cost"
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return {
        "message": "Recipe creation failed!",
        "required": "title, making_time, serves, ingredients, cost"
    }

@app.post('/recipes', status_code=200)
def create_recipe(recipe_create: RecipeCreate, db: Session = Depends(get_db)):

    try:
        # db_recipe = recipe(**recipe_create.dict())
        db_recipe = recipe()
        for key, value in recipe_create.dict(exclude_unset=True).items():
            setattr(db_recipe, key, value)

        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        if db_recipe is None:
            return {
                "message": "Recipe creation failed!",
                "required": "title, making_time, serves, ingredients, cost"
            }
        return {
            "message": "Recipe successfully created!",
            "recipe": db_recipe
        }
    except SQLAlchemyError as e:
        return {
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }
        
'''
  {
    "message": "Recipe successfully updated!",
    "recipe": [
      {
        "title": "トマトスープレシピ",
        "making_time": "15分",
        "serves": "5人",
        "ingredients": "玉ねぎ, トマト, スパイス, 水",
        "cost": "450"
      }
    ]
  }
'''
@app.patch('/recipes/{recipe_id}')
def update_recipe(recipe_id: str, recipe_update: RecipeUpdate, db: Session = Depends(get_db)):
    try:
        db_recipe = db.query(recipe).filter(recipe.id == recipe_id).first()
        if db_recipe is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

        for key, value in recipe_update.dict(exclude_unset=True).items():
            setattr(db_recipe, key, value)

        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    finally:
        db.refresh(db_recipe)
        return {
            "message": "Recipe successfully updated!",
            "recipe": db_recipe
        }

'''
{  "message": "Recipe successfully removed!" }
OR
{ "message":"No Recipe found" }
'''
@app.delete('/recipes/{recipe_id}')
def delete_recipe(recipe_id: str, db: Session = Depends(get_db)):
    db_recipe = db.query(recipe).filter(recipe.id == recipe_id).first()
    if db_recipe is None:
        return {
            "message":"No Recipe found"
        }
    db.delete(db_recipe)
    db.commit()
    return {
        "message": "Recipe successfully removed!"
    }
