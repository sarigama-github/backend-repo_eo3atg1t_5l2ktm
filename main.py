import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents, db
from schemas import Client, Project, Milestone, Update, Celebration

app = FastAPI(title="Xperience Hub Client Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Xperience Hub API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Simple create-and-list endpoints to power the portal demo

@app.post("/api/clients", response_model=dict)
def create_client(client: Client):
    try:
        inserted_id = create_document("client", client)
        return {"id": inserted_id, "message": "Client created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clients", response_model=List[dict])
def list_clients(limit: Optional[int] = 20):
    try:
        docs = get_documents("client", limit=limit)
        # Convert ObjectId to string for frontend display
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects", response_model=dict)
def create_project(project: Project):
    try:
        inserted_id = create_document("project", project)
        return {"id": inserted_id, "message": "Project created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects", response_model=List[dict])
def list_projects(limit: Optional[int] = 20):
    try:
        docs = get_documents("project", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/updates", response_model=dict)
def create_update(update: Update):
    try:
        inserted_id = create_document("update", update)
        return {"id": inserted_id, "message": "Update created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/updates", response_model=List[dict])
def list_updates(limit: Optional[int] = 20):
    try:
        docs = get_documents("update", limit=limit)
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
