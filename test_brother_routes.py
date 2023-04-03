from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Brother, BrotherUpdate

router = APIRouter()

def format_names(name):
    name = name.upper()
    return name

@router.get("/", response_description="List all brothers", response_model=List[Brother])
def list_brothers_test(request: Request):
    # document_size = int(request.app.database["brothers"].count_documents({}))
    #document_size = request.app.brother_documents_size
    #size = request.app.test_database["brothers"].countDocuments
    rec = request.app.test_database["assembly"].find({})
    assemblies_names = [x["name"] for x in rec]
    brothers = []
    for x in assemblies_names:
        brethen = list(request.app.test_database["brothers"].find({"assembly": x}))
        brothers = brothers + brethen
    #brothers = list(request.app.test_database["brothers"].find({"assembly": "Joinville"}))
    #brothers = res
    return brothers



