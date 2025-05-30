from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from google.genai import types


class BillData(BaseModel):
  item: str = Field(..., description="Name of item purchased")
  quantity: int = Field(..., description="Quantity of item purchased")
  price_per_quant: float = Field(..., description="Price per quantity of item purchased")
  total_amount: float = Field(..., description="Total amount of the item purchased")
  date: str = Field(..., description="Date of the bill")
  seller: str = Field(..., description="Name of the seller or store")
  tax: float = Field(..., description="Tax applied on the bill")
  category: str = Field(..., description="Category of the item purchased")
  payment_method: str = Field(..., description="Payment method used for the bill")


load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
client = genai.Client(
  vertexai=True,project=PROJECT_ID, location=LOCATION,
)
# If your image is stored in Google Cloud Storage, you can use the from_uri class method to create a Part object.
IMAGE_URI = "gs://finapp_nk/data/shoppers_bill.pdf.pdf"
model = "gemini-2.0-flash-001"

def process_request():
    response = client.models.generate_content(
        model=model,
        contents=[
            USER_PROMPT,
            types.Part.from_uri(
                file_uri=IMAGE_URI,
                mime_type="application/pdf",
            ),
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=5000,
            temperature=0.1,
            top_p=0.5,
            response_schema=BillData,
            response_mime_type="application/json",
        )
    )
 
    return response.text

if __name__ == "__main__":
    USER_PROMPT = "This is a bill is : "
    SYSTEM_PROMPT = """You are a data extraction assistant that extracts the required data fields from a bill. The bill is provided as an image or PDF file. 
    Please output only the information/data actually present in the bill."""
    print("Processing request...")
    result = process_request()
    print(f"Result: {result}")