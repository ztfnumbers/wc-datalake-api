from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from api.brother_routes import router as brother_router
from api.assembly_routes import router as assembly_router
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")

app = FastAPI()

origins = ["*"] # TODO: add the right front end's IP adress

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(brother_router, tags=["brothers"], prefix="/brother")
app.include_router(assembly_router, tags=["assemblies"], prefix="/assembly")
