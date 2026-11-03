from fastapi import FastAPI
from routes import analyse



app = FastAPI(
    title="Vision AI", 
    description="AI powered crop disease detection using computer vision", 
    version="1.0.0")

app.include_router(analyse.router)


@app.get("/")
async def root():
    return {
        "app_name": "Vision AI Crop Disease Detection API",
        "message": "Welcome to Vision AI Crop Disease Detection API!",
        "endpoints": {
            "POST /analyse": "Upload an image for disease detection",
            "POST /analyse/batch": "Upload multiple images for batch disease detection",
            "GET /analyses": "Retrieve a list of all analyses performed",
            "GET /analyses/{analysis_id}": "Retrieve details of a specific analysis by ID"
        }
        }