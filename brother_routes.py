from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId

from models import Brother, BrotherUpdate

router = APIRouter()

def format_names(name):
    name = name.upper()
    return name

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
    # document_size = int(request.app.database["brothers"].count_documents({}))
    #document_size = request.app.brother_documents_size
    rec = request.app.database["assembly"].find({})
    assemblies_names = [x["name"] for x in rec]
    brothers = []
    for x in assemblies_names:
        brethen = list(request.app.database["brothers"].find({"assembly": x}))
        brothers = brothers + brethen
    return brothers



@router.get("/{id}", response_description="Get a single brother by id", response_model=Brother)
def find_brother(id: str, request: Request):
    #id = ObjectId(id)
    if (brother := request.app.database["brothers"].find_one({"_id": id})) is not None:
        brother["name"] = format_names(brother["name"])
        #brother["_id"] = str(brother["_id"])
        return brother
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brother with ID {id} not found")


@router.get("/member_of/{assembly_name}", response_description="List all brothers belonging to the specified assembly", response_model=List[Brother])
def find_assembly_brothers(assembly_name: str, request: Request):
    brothers = list(request.app.database["brothers"].find({"assembly": assembly_name}))
    if(len(brothers) > 0):
        for x in brothers:
            x["name"] = format_names(x["name"])    
            #x["_id"] = str(x["_id"])
        return brothers
    else:
        return []
    #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Assembly {assembly_name} has no brothers")


@router.get("/leaders/", response_description="List all leaders", response_model=List[Brother])
def get_leaders(request: Request):
    brothers = list(request.app.database["brothers"].find({"statut": "Dirigeant"}))
    if(len(brothers) > 0):
        for x in brothers:
            x["name"] = format_names(x["name"])
            #x["_id"] = str(x["_id"])        
        return brothers
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No leaders")



@router.put("/{id}", response_description="Update a brother", response_model=Brother)
def update_brother(id: str, request: Request, brother: BrotherUpdate = Body(...)):
    #id = repr(ObjectId(id))
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
    #id = ObjectId(id)
    delete_result = request.app.database["brothers"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Brother with ID {id} not found")
