import os
from uuid import uuid4
from PIL import Image
from io import BytesIO

class PhotoService:
    def __init__(self):
        self.upload_dir = "uploads/photos"
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_photo(self, file_content: bytes) -> str:
        try:
            # Validate image
            img = Image.open(BytesIO(file_content))
            
            # Generate unique filename
            filename = f"{uuid4()}.jpg"
            filepath = os.path.join(self.upload_dir, filename)
            
            # Save standardized image
            img = img.convert('RGB')
            img.save(filepath, 'JPEG')
            
            return filepath
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}") 