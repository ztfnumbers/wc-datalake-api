from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Brothers, BrothersUpdate, Assemblies, AssembliesUpdate

router = APIRouter()

@router.post("/", response_description="Create a new brother", status_code=status.HTTP_201_CREATED, response_model=Brother)
def create_brother(request: Request, brother: Brother = Body(...)):
    brother = jsonable_encoder(brother)
    new_brother = request.app.database["brothers"].insert_one(brother)
    created_brother = request.app.database["brothers"].find_one(
        {"_id": new_brother.inserted_id}
    )
    return created_brother


@router.get("/", response_description="List all brothers", response_model=List[Brother])
def list_brothers(request: Request):
    brothers = list(request.app.database["brothers"].find(limit=100))
    return brothers


@router.get("/{id}", response_description="Get a single brother by id", response_model=Brother)
def find_brother(id: str, request: Request):
    if (brother := request.app.database["brothers"].find_one({"_id": id})) is not None:
        return brother
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brother with ID {id} not found")




@router.put("/{id}", response_description="Update a brother", response_model=Brother)
def update_brother(id: str, request: Request, brother: BrotherUpdate = Body(...)):
    brother = {k: v for k, v in brother.dict().items() if v is not None}
    if len(brother) >= 1:
        update_result = request.app.database["brothers"].update_one(
            {"_id": id}, {"$set": brother}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brother with ID {id} not found")

    if (
        existing_brother := request.app.database["brothers"].find_one({"_id": id})
    ) is not None:
        return existing_brother

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brother with ID {id} not found")




@router.delete("/{id}", response_description="Delete a brother")
def delete_brother(id: str, request: Request, response: Response):
    delete_result = request.app.database["brothers"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brother with ID {id} not found")
