from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
from brother_routes import router as brother_router
from assembly_routes import router as assembly_router

configu = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    configu["ATLAS_URI"] = "mongodb+srv://silas:holylord2.@cluster0.lumkhyn.mongodb.net/?retryWrites=true&w=majority"
    configu["DB_NAME"] = "pymongo_tutorial"
    app.mongodb_client = MongoClient(configu["ATLAS_URI"])
    app.database = app.mongodb_client[configu["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(brother_router, tags=["brothers"], prefix="/brother")
app.include_router(assembly_router, tags=["assemblies"], prefix="/assembly")
