from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import secrets

app = FastAPI(title="ResolveIT AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. SECURITY ---
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, "admin")
    correct_pass = secrets.compare_digest(credentials.password, "resolveit")
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail="Incorrect credentials", headers={"WWW-Authenticate": "Basic"})
    return credentials.username

# --- DYNAMIC COUNTER ---
query_count = 0

# --- 2. LOAD AI BRAIN ---
print("Loading FAISS database...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
print("Database loaded successfully!")

class Question(BaseModel):
    query: str

# --- 3. PAGES & API ENDPOINTS ---

@app.get("/")
def read_root(user: str = Depends(get_current_user)):
    return FileResponse("index.html")

@app.get("/runbooks")
def read_runbooks_page(user: str = Depends(get_current_user)):
    return FileResponse("runbooks.html")

@app.get("/api/runbooks")
def get_runbooks(category: str = "", user: str = Depends(get_current_user)):
    if not category:
        return JSONResponse(content={"runbooks": []})
    results = db.similarity_search(f"--- CATEGORY: {category} ---", k=15)
    clean_results = []
    for doc in results:
        text = doc.page_content.strip()
        if len(text) > 100 and "Resolution Steps" in text:
            clean_results.append(text)
    return JSONResponse(content={"runbooks": clean_results})

@app.get("/api/stats")
def get_stats(user: str = Depends(get_current_user)):
    global query_count
    total_chunks = db.index.ntotal
    return {
        "total_chunks": total_chunks,
        "query_count": query_count,
        "system_status": "Operational"
    }

@app.post("/ask")
def ask_runbook(question: Question, user: str = Depends(get_current_user)):
    global query_count
    query_count += 1 # Increment on every question
    
    print(f"User '{user}' asked: {question.query}")
    results = db.similarity_search(question.query, k=3)
    best_match = "\n\n---\n\n".join([doc.page_content for doc in results])
    
    ai_response = f"""I found the exact runbook for this issue. Please follow these steps:

**{best_match}**

---
*Let me know if you need further assistance!*"""

    return {"answer": ai_response}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)