from fastapi import FastAPI
import json

app = FastAPI()

with open("../data.json") as j:
    data = json.load(j)

data_len = len(data)


@app.get("/json-data")
def read_data(page: int = 1, per_page: int = 10):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]
