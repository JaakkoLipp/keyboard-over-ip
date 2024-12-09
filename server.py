from fastapi import FastAPI, Body

app = FastAPI()

last_input = None

# MVP, websocket or kafka msg queue system l8r

@app.post("/input")
def post_input(data: dict = Body(...)):
    global last_input
    last_input = data
    return {"status": 200, "message": "Input stored successfully"}

@app.get("/output")
def read_output():
    global last_input
    if last_input:
        return last_input
    else:
        return {"status": 404, "message": "No input available"}
