import sys
import os


import certifi
ca = certifi.where()


from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
import pymongo

from src.logging.logger import logging
from src.exception.exception import networkException
from src.pipelines.training_pipeline import TrainingPipeline
from src.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI , File, UploadFile , Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd


from src.utils.main_utils.utils import load_object

from src.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME , DATA_INGESTION_DATABASE_NAME
from src.entity.config_entity import trainingPipelineConfig
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
db = client[DATA_INGESTION_DATABASE_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/" , tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train" , tags=["training"])
async def train():
    try:
        logging.info("Training pipeline started...")
        training_pipeline = TrainingPipeline(trainingPipelineConfig())
        training_pipeline.run()
        logging.info("Training pipeline completed successfully.")
        return {"message": "Training completed successfully."}
    except Exception as e:
        logging.error(f"An error occurred during training: {e}")
        raise networkException(e, sys)
    

@app.get("/predict" , tags=["prediction"])
async def perdict_route(request: Request , file: UploadFile = File(...)):
    try:

        df = pd.read_csv(file.file)

        logging.info("Loading model for prediction...")
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        logging.info("Model loaded successfully.")

        network_model = NetworkModel(preprocessor=preprocessor, model=model)

        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df["predicted_column"])
        df.to_csv("prediction_output/predicted_output.csv", index=False)
        table_html = df.to_html(classes='table table-striped', index=False)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
    except Exception as e:
        logging.error(f"An error occurred while loading the model: {e}")
        raise networkException(e, sys)
    
if __name__ == "__main__":
    try:
        logging.info("Starting the FastAPI application...")
        app_run(app, host="localhost", port=8000)
    except Exception as e:  
        logging.error(f"An error occurred while starting the FastAPI application: {e}")
        raise networkException(e, sys)






