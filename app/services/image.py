from email.mime import image
import io
import os
from turtle import width
from PIL import Image
from config import ALLOWED_IMAGE_TYPES, MAX_IMAGE_DIMENSIONS, MAX_IMAGE_SIZE_MB


def validate_image(content: bytes, content_type: str| None) -> dict:
    """
    Validate the image file.

    Args:
        content: The image content to validate.
        content_type: The content type of the image.

    Returns:
        dict: A dictionary containing the validation result and image dimensions if valid.
    """
    # Check if the image is None
    if content is None:
        return {"is_valid": False, "error": "Image content is None"}
    if content_type is None:
        return {"is_valid": False, "error": "Image content type is None"}
    if not content_type.startswith("image/"):
        return {"is_valid": False, "error": "Invalid image content type"}



    # Check if the image has a valid content type
   
    if content_type not in ALLOWED_IMAGE_TYPES:
        return {"is_valid": False, "error": "Image content type is not allowed"}

    # Check if the image size is within limits (e.g., 15MB)

    size_mb = len(content) / (1024 * 1024)  # Convert bytes to MB
    if size_mb > MAX_IMAGE_SIZE_MB:
        return {"is_valid": False, "error": "Image size exceeds the limit"}

    image = Image.open(io.BytesIO(content))
    image.verify()  # Verify that the image is valid
    width, height = image.size


    return {
            "is_valid": True, 
            "message": "Image is valid", 
            "width": width,
             "height": height,
             "size_mb": size_mb
             }

def resize_image_if_needed(image) -> Image.Image:
    width, height = image.size
    if width > MAX_IMAGE_DIMENSIONS[0] or height > MAX_IMAGE_DIMENSIONS[1]:
        resized_image = image.copy()
        resized_image.thumbnail(MAX_IMAGE_DIMENSIONS)
        return resized_image
    return image

def save_image(image: Image.Image, path: str, filename: str) -> str:
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    with open(file_path, "wb") as f:
        image.save(f, format=image.format)
    return file_path