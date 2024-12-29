from fastapi import APIRouter, HTTPException
import base64
from io import BytesIO
from PIL import Image
from apps.calculator.utils import analyze_image
from schema import ImageData

router = APIRouter()

@router.post("/")
async def run(data: ImageData):
    """
    Processes a base64-encoded image, analyzes it, and returns the results.
    
    Args:
        data (ImageData): The input data containing a base64-encoded image and additional variables.
    
    Returns:
        dict: A response indicating success or failure with the processed data.
    """
    try:
        # Decode the base64 image string
        if not data.image.startswith("data:image"):
            raise ValueError("Invalid image format. Must include 'data:image/<type>;base64,'.")
        
        # Remove the prefix (e.g., "data:image/png;base64,")
        image_data = base64.b64decode(data.image.split(",")[1])
        image_bytes = BytesIO(image_data)
        
        # Open the image with PIL
        image = Image.open(image_bytes)
        
        # Analyze the image using a utility function
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        processed_data = []
        
        for response in responses:
            processed_data.append(response)
        
        print("Response in route: ", responses)  # For debugging
        
        return {"message": "Image processed successfully", "data": processed_data, "status": "success"}
    
    except Exception as e:
        # Handle errors and return a meaningful message
        print(f"Error processing image: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")
