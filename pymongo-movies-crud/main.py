from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as movie_router
from neo4j import GraphDatabase #added

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    #on utilise les informations de connections définies en .env
    app.mongodb_client = MongoClient(config["MONGODB_URL"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    #added
    app.neo4j_driver = GraphDatabase.driver(
        config["NEO4J_URI"], 
        auth=(config["NEO4J_USERNAME"], config["NEO4J_PASSWORD"])
    )

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.neo4j_driver.close()


app.include_router(movie_router, tags=["movies"], prefix="/movie")