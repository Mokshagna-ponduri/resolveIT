# 🛠️ ResolveIT AI

> **AI-powered IT helpdesk assistant with a semantic runbook search engine.**

ResolveIT AI is a full-stack application that uses vector embeddings and semantic similarity search to instantly retrieve the correct resolution steps for any IT issue. Instead of digging through sprawling wikis or waiting for a technician, support staff can describe a problem in plain English and receive step-by-step resolution guidance in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Resolution Engine** | Chat interface for describing IT issues and receiving exact runbook steps |
| 📚 **Runbook Database** | Browsable library of runbooks, filterable by 6 IT categories |
| 📊 **Live Dashboard** | Real-time stats: vector chunk count, query count, latency & accuracy |
| 🔍 **Semantic Search** | FAISS vector store powered by `all-MiniLM-L6-v2` HuggingFace embeddings |
| 🔐 **HTTP Basic Auth** | Password-protected access to keep the interface internal-only |
| 🎨 **Modern UI** | Dark glassmorphism design with animated background effects |

---

## 🖼️ Application Overview

The app is divided into three sections accessible from the sidebar:

- **Dashboard** — System health at a glance with bar charts, a query-distribution donut chart, a live activity feed, and a top-issues table.
- **AI Assistant** — Chat window where you describe your problem and get the matching runbook steps instantly.
- **Runbook DB** — Visual card-grid view of all runbooks, filterable by category.

---

## 🏗️ Architecture

```
┌────────────────────────────────────┐
│          Browser (index.html)      │  ← Single-file dark UI (Vanilla JS + CSS)
└──────────────┬─────────────────────┘
               │ HTTP (Basic Auth)
┌──────────────▼─────────────────────┐
│         FastAPI Backend (main.py)  │
│  GET  /              → index.html  │
│  POST /ask           → AI answer   │
│  GET  /api/runbooks  → runbook list│
│  GET  /api/stats     → live stats  │
│  GET  /health        → health check│
└──────────────┬─────────────────────┘
               │
┌──────────────▼─────────────────────┐
│    FAISS Vector Store (faiss_index)│  ← Built by ingest.py
│    Embedding: all-MiniLM-L6-v2     │
│    Source Data: data/all_manuals.txt│
└────────────────────────────────────┘
```

---

## 📋 Runbook Categories

| Category | Examples |
|---|---|
| 🖥️ Hardware & End-User Devices | Laptop won't turn on, BSOD, USB not recognized |
| 🌐 Network & Connectivity | Wi-Fi dropping, DNS errors, IP conflicts |
| 💻 Software & Applications | App freezing, Windows Update stuck, Office crashes |
| 🔒 Security & Access | MFA failures, phishing reports, password resets |
| 🗄️ Server & Infrastructure | High CPU, disk full, SSL cert expired, DB timeouts |
| 📧 Communications (Email & Chat) | Teams not loading, Outlook PST too large, audio issues |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resolveit-ai.git
cd resolveit-ai
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn langchain langchain-community langchain-huggingface faiss-cpu sentence-transformers
```

### 3. Build the vector database

Run this **once** to embed all runbooks and create the FAISS index:

```bash
python ingest.py
```

> ⏳ The first run downloads the `all-MiniLM-L6-v2` embedding model (~80 MB). Subsequent runs are fast.

Expected output:
```
Starting runbook ingestion...
Loaded: all_manuals.txt
Split runbooks into XX chunks.
Loading embedding model...
Creating FAISS index...
Success! FAISS index saved to 'faiss_index' folder.
```

### 4. Start the server

```bash
uvicorn main:app --reload
```

### 5. Open the app

Navigate to [http://localhost:8000](http://localhost:8000) and log in with:

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `resolveit` |

> ⚠️ **Security Note:** Change the hardcoded credentials in `main.py` before deploying to any production or shared environment.

---

## 📁 Project Structure

```
resolveit-ai/
├── main.py          # FastAPI backend — API routes, auth, FAISS queries
├── ingest.py        # One-time script to build the FAISS vector index
├── index.html       # Complete single-file frontend (HTML + CSS + JS)
├── data/
│   └── all_manuals.txt   # Source runbook data (plain text, structured)
└── faiss_index/          # Generated FAISS index (created by ingest.py)
```

---

## ➕ Adding Your Own Runbooks

1. Open `data/all_manuals.txt`.
2. Follow the existing format:

```
--- CATEGORY: YOUR CATEGORY NAME ---

Troubleshooting: Issue Title
Symptoms: What the user sees.
Root Cause: Why this happens.
Resolution Steps:
1. Step one.
2. Step two.
...

---
```

3. Re-run `python ingest.py` to rebuild the vector index.
4. Restart the server.

---

## 🔌 API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/` | ✅ | Serve the main UI |
| `POST` | `/ask` | ✅ | Query the AI with an IT issue |
| `GET` | `/api/runbooks?category=...` | ✅ | Fetch runbooks by category |
| `GET` | `/api/stats` | ✅ | Get vector chunk count & query count |
| `GET` | `/health` | ❌ | Health check (no auth required) |

### Example: `/ask` Request

```bash
curl -u admin:resolveit -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "my laptop has a blue screen with error code"}'
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) |
| Embeddings | [HuggingFace — all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| Vector DB | [FAISS](https://github.com/facebookresearch/faiss) |
| LangChain | Document loading, text splitting, vector store abstraction |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Markdown Rendering | [marked.js](https://marked.js.org/) |
| Fonts | Google Fonts — Inter |

---

## 🔮 Potential Improvements

- [ ] Swap FAISS similarity search for a true LLM (e.g. GPT-4o, Gemini, Llama 3) to generate conversational answers
- [ ] Add a ticket logging system (save queries + resolutions to a database)
- [ ] Role-based access control (admin vs. read-only)
- [ ] Upload new runbooks through the UI without editing text files
- [ ] Docker container for one-command deployment
- [ ] Automated runbook accuracy feedback loop

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ for IT support teams who deserve better tools.</p>
