from typing import List, Any

from fastapi import APIRouter, Request
from models.note import Note
from config.db import conn
from schemas.note import noteEntity, notesEntity
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

note = APIRouter()

templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newdocs: list[Any] = []
    for doc in docs:
        try:
            validated_doc = Note(
                id=doc["_id"],
                title=doc.get("title"),
                priority=doc.get("priority"),
                desc=doc.get("desc")
            )
            newdocs.append(validated_doc.dict())
        except ValueError as e:
            print(f"Error processing document with _id={doc['_id']}: {e}")

        print(doc)
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newdocs})


@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    note = conn.notes.notes.insert_one(dict(form))
    return {"Success"}
