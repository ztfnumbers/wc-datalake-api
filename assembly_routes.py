from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Assembly, AssemblyUpdate
from bson import ObjectId


router = APIRouter()

@router.post("/", response_description="Create a new assembly", status_code=status.HTTP_201_CREATED, response_model=Assembly)
def create_assembly(request: Request, assembly: Assembly = Body(...)):
    assembly = jsonable_encoder(assembly)
    new_assembly = request.app.database["assembly"].insert_one(assembly)
    created_assembly = request.app.database["assembly"].find_one(
        {"_id": new_assembly.inserted_id}
    )
    return created_assembly


@router.get("/", response_description="List all assemblies", response_model=List[Assembly])
def list_assemblies(request: Request):
    assemblys = list(request.app.database["assembly"].find({}))
    return assemblys


@router.get("/{id}", response_description="Get a single assembly by id", response_model=Assembly)
def find_assembly(id: str, request: Request):
    id = ObjectId(id)
    if (assembly := request.app.database["assembly"].find_one({"_id": id})) is not None:
        #assembly["_id"] = str(assembly["_id"])
        return assembly
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assembly with ID {id} not found")




@router.put("/{id}", response_description="Update a assembly", response_model=Assembly)
def update_assembly(id: str, request: Request, assembly: AssemblyUpdate = Body(...)):
    assembly = {k: v for k, v in assembly.dict().items() if v is not None}
    if len(assembly) >= 1:
        update_result = request.app.database["assembly"].update_one(
            {"_id": id}, {"$set": assembly}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assembly with ID {id} not found")

    if (
        existing_assembly := request.app.database["assembly"].find_one({"_id": id})
    ) is not None:
        return existing_assembly

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assembly with ID {id} not found")




@router.delete("/{id}", response_description="Delete a assembly")
def delete_assembly(id: str, request: Request, response: Response):
    delete_result = request.app.database["assembly"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assembly with ID {id} not found")
