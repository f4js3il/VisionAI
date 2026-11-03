from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
MAX_IMAGE_SIZE_MB = 15
MAX_IMAGE_DIMENSIONS = (1024, 1024)  # Maximum width and height in pixels
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")  # Must be a vision-capable model