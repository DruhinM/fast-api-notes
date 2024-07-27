from fastapi import FastAPI
from routes.note import note

app = FastAPI()

# Include the APIRouter
app.include_router(note)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
