from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from brother_routes import router as brother_router
from test_brother_routes import router as test_brother_router
from assembly_routes import router as assembly_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    app.test_database = app.mongodb_client[config["TEST_DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(brother_router, tags=["brothers"], prefix="/brother")
app.include_router(test_brother_router, tags=["brothers"], prefix="/test/brother")
app.include_router(assembly_router, tags=["assemblies"], prefix="/assembly")