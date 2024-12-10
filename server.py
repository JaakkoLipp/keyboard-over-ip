from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for keystroke data
# Not very good but works for demo purposes
last_input = None


# Input data model
class Keystroke(BaseModel):
    input: str


@app.post("/input")
async def post_input(data: Keystroke):
    """
    Endpoint to receive input (keystrokes) from the producer.
    """
    global last_input
    last_input = data.input
    return {"status": 200, "message": "Input stored successfully"}


@app.get("/output")
async def read_output():
    """
    Endpoint to retrieve the last input for the reader.
    """
    global last_input
    if last_input is None:
        return {"status": 404, "message": "No input available"}
    return {"input": last_input}

@app.get("/")
async def root():
    """Test endpoint for root"""
    return {"message": "Keyboard-over-internet backend is running!"}
