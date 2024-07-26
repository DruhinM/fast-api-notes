import ssl

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

client = MongoClient("mongodb+srv://user:3womVd6pvH6Lt46Z@notes.8kdkaxg.mongodb.net")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = client.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "note": doc["note"]

        })

        print(doc)
    return templates.TemplateResponse("index.html", {"request": request,"newDocs": newDocs })

