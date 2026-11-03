from fastapi import APIRouter, File, HTTPException, UploadFile
from services.vision import analyse_crop_image
from services.image import save_image, validate_image, resize_image_if_needed
from PIL import Image
import io
import uuid




router = APIRouter(prefix="/analyse", tags=["Analyse"]) 

async def process_single_image(file: UploadFile):
  content = await file.read()
  validation_result = validate_image(content, file.content_type)
  if not validation_result["is_valid"]:
      raise HTTPException(status_code=400, detail=validation_result["error"])
  
  image = Image.open(io.BytesIO(content))
  processed_image = resize_image_if_needed(image)
  extension = processed_image.format.lower() if processed_image.format else 'png'
  
  unique_filename = f"{uuid.uuid4().hex}.{extension}"
  save_image(processed_image, "uploads", unique_filename)  
  result = await analyse_crop_image(processed_image)  # Call the analysis function
  return result


@router.post("/")
async def analyse_image(file: UploadFile = File(...)):
    """
    Endpoint to analyse a single image for crop disease detection.
    """
    result = await process_single_image(file)

    # Logic for analysing the image will go here
    return {"message": "Image analysis endpoint", "result": result}

@router.post("/batch")
async def analyse_batch_images(files: list[UploadFile] = File(...)):
    """
    Endpoint to analyse multiple images for crop disease detection.
    """
    results = []
    for file in files:
        result = await process_single_image(file)
        results.append(result)
    
    return {"message": "Batch image analysis endpoint", "results": results}


