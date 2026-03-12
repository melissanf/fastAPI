from fastapi import FastAPI , Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
#ressource video https://www.youtube.com/watch?v=NcPQm2KkIWE&t=305s
# defining a Pydantic model to represent the response of the BMI calculation
class BMIRequest(BaseModel):
    bmi : float
    message : str
# creating an instance of the FastAPI class to create our API
app = FastAPI()
# adding CORS (Cross-Origin Resource Sharing) middleware to allow requests from any origin, which is useful for testing the API from different clients or front-end applications.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# defining a route for the root URL ("/") and associating it with the Hi function default route 
@app.get("/")
# defining the Hi function that will be called when the root URL is accessed
def Hi():
    return {"message": "Hello World!"}
#passing data to the API in this way
# http://127.0.0.1:8000/calculate_bmi?weight=90&height=1.64
@app.get("/calculate_bmi")
def calculate_BMI(
    weight: float = Query(..., gt=20, lt=200, description="Weight in kilograms"),
    height: float = Query(..., gt=1.0, lt=2.5, description="Height in meters")  
    ):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        message = "Category: Underweight"
    elif 18.5 <= bmi < 24.9:
        message = "Category: Normal weight"
    elif 25 <= bmi < 29.9:
        message = "Category: Overweight"
    else:        message = "Category: Obesity"
    return BMIRequest(bmi=bmi, message=message)

#automatic documentation of the API a known feature of FASTAPI is that it automatically generates documentation for the API using OpenAPI and Swagger UI.
# To access the documentation, http://127.0.0.1:8000/docs

#automatic validation of input data in fastapi is done using query in parameters if its obligatoire we add Query(...) if its optional we add Query(None) and we can also add constraints like gt (greater than) and lt (less than) to ensure that the input data is valid.
""" an example of the error message that would be returned if the input data does not meet the specified constraints is as follows:
{
  "detail": [
    {
      "type": "greater_than",
      "loc": [
        "query",
        "weight"
      ],
      "msg": "Input should be greater than 20",
      "input": "19",
      "ctx": {
        "gt": 20
      }
    },
    {
      "type": "less_than",
      "loc": [
        "query",
        "height"
      ],
      "msg": "Input should be less than 2.5",
      "input": "3.20",
      "ctx": {
        "lt": 2.5
      }
    }
  ]
}
"""
# pydantic is a library used by FastAPI for data validation and settings management using Python type annotations. It allows you to define data models with type hints, and it automatically validates the input data against those models. In this code, we are using Pydantic's Query class to define the expected input parameters for the calculate_BMI function, along with constraints on their values.
