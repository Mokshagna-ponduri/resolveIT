import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_FOLDER = "data"
DB_INDEX_PATH = "faiss_index"

def ingest_runbooks():
    print("Starting runbook ingestion...")
    
    documents = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_FOLDER, filename)
            loader = TextLoader(filepath)
            documents.extend(loader.load())
            print(f"Loaded: {filename}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Split runbooks into {len(chunks)} chunks.")

    print("Loading embedding model (this might take a minute the first time)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Creating FAISS index...")
    vector_db = FAISS.from_documents(chunks, embeddings)

    vector_db.save_local(DB_INDEX_PATH)
    print(f"Success! FAISS index saved to '{DB_INDEX_PATH}' folder.")

if __name__ == "__main__":
    ingest_runbooks()