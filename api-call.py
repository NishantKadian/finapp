from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from google.genai import types
import json

# Define the pydantic model to extract data from the bill
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

class BillDataResponse(BaseModel):
  bill_data: list[BillData] = Field(..., description="Extracted data from the bill")
 
 # Load environment variables
load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")

# Define the model to be used for extraction
model = "google/gemini-2.5-flash-preview-05-20"

# Initialize the GenAI client
client = genai.Client(
  vertexai=True,project=PROJECT_ID, location=LOCATION,
)

# extraction logic 
def process_request(file_path: str):

    """ read a PDF file and extract data from it using Google GenAI """
    with open(file_path, 'rb') as file:
        f_bytes = file.read()

    """ Create a Part object from the file bytes """
    cont = types.Part.from_bytes(
        data=f_bytes,
        mime_type="application/pdf"
    )

    response = client.models.generate_content(
        model=model,
        contents=[ "Here is the bill :\n",
            cont
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=5000,
            temperature=0.1,
            top_p=0.5,
            response_schema=BillDataResponse,
            response_mime_type="application/json",
        )
    )
 
    return response.text

if __name__ == "__main__":
    SYSTEM_PROMPT = """You are a data extraction assistant that extracts the required data fields from a bill. The bill is provided as an image or PDF file. 
    Please output only the information/data actually present in the bill."""
    print("Processing request...")

    result = process_request(r"C:\Users\nisha\nk_workspace\pdf-extraction\data\bills\bill3.pdf")
    try:
        parsed_result = json.loads(result)
        pretty_result = json.dumps(parsed_result, indent=4)
        print("Result:")
        print(pretty_result)
    except Exception as e:
        print("Failed to parse result as JSON. Raw output:")
        print(result)

# data credits : https://www.kaggle.com/datasets/jenswalter/receipts/