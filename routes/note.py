from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Any, List
from bson.objectid import ObjectId

from models.note import Note  # Import the Note model
from config.db import conn  # Import the database connection
from schemas.note import noteEntity, notesEntity  # Import the schemas

note = APIRouter()

templates = Jinja2Templates(directory="templates")
collection = conn.notes


@note.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    docs = collection.find({})
    new_docs: List[Any] = []
    for doc in docs:
        try:
            validated_doc = Note(
                id=str(doc["_id"]),
                title=doc.get("title"),
                priority=doc.get("priority"),
                desc=doc.get("desc")
            )
            new_docs.append(validated_doc.dict())
        except ValueError as e:
            print(f"Error processing document with _id={doc['_id']}: {e}")

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": new_docs})


@note.get("/search", response_class=HTMLResponse)
async def search_items(request: Request, query: str = Query(...)):
    docs = collection.find({"$or": [
        {"title": {"$regex": query, "$options": "i"}},
        {"desc": {"$regex": query, "$options": "i"}}
    ]})
    new_docs: List[Any] = []
    for doc in docs:
        try:
            validated_doc = Note(
                id=str(doc["_id"]),
                title=doc.get("title"),
                priority=doc.get("priority"),
                desc=doc.get("desc")
            )
            new_docs.append(validated_doc.dict())
        except ValueError as e:
            print(f"Error processing document with _id={doc['_id']}: {e}")

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": new_docs})


@note.get("/filter", response_class=HTMLResponse)
async def filter_items(request: Request, priority: int = Query(...)):
    docs = collection.find({"priority": priority})
    new_docs: List[Any] = []
    for doc in docs:
        try:
            validated_doc = Note(
                id=str(doc["_id"]),
                title=doc.get("title"),
                priority=doc.get("priority"),
                desc=doc.get("desc")
            )
            new_docs.append(validated_doc.dict())
        except ValueError as e:
            print(f"Error processing document with _id={doc['_id']}: {e}")

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": new_docs})


@note.post("/", response_class=RedirectResponse)
async def create_item(request: Request):
    form = await request.form()
    note_data = {
        "title": form.get("title"),
        "priority": int(form.get("priority", 0)),
        "desc": form.get("desc")
    }
    collection.insert_one(note_data)
    return RedirectResponse(url="/", status_code=303)


@note.get("/get-item/{item_id}", response_class=JSONResponse)
async def get_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return noteEntity(item)
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@note.post("/update-item", response_class=RedirectResponse)
async def update_item(id: str = Form(...), title: str = Form(...), desc: str = Form(...), priority: int = Form(...)):
    collection.update_one({"_id": ObjectId(id)}, {"$set": {"title": title, "desc": desc, "priority": priority}})
    return RedirectResponse(url="/", status_code=303)


@note.post("/delete-note", response_class=RedirectResponse)
async def delete_note(item_id: str = Form(...)):
    collection.delete_one({"_id": ObjectId(item_id)})
    return RedirectResponse(url="/", status_code=303)
