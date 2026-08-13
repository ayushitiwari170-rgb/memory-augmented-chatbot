# Memory-Augmented Chatbot with Knowledge Graph and Hybrid RAG System

## Overview

This project implements a hybrid conversational AI system that combines three distinct
intelligence layers to answer user queries:

1. **Retrieval-Augmented Generation (RAG)** — answers grounded in a static knowledge base
2. **Knowledge Graph (KG)** — structured entity-relationship reasoning
3. **Memory** — persistent, per-user long-term context across conversations
4. **Dynamic Tools** — live external data (e.g. real-time weather) via API calls

A **LangGraph** orchestration layer decides, per query, which of these subsystems should
handle the response.

---

## Problem Statement

Traditional chatbots either rely purely on static document retrieval (RAG) or purely on
live API calls, and rarely retain any memory of the user across turns. This project
demonstrates a system that unifies all three: it recalls user-specific facts, reasons over
structured relationships between entities, and can still fetch real-time data when needed —
routed dynamically through a single conversational interface.

---

## Architecture

```
                         ┌─────────────────────┐
                         │      User Query      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LangGraph Router    │
                         │  (conditional entry)  │
                         └──────────┬───────────┘
                    ┌───────────────┼───────────────┬───────────────┐
                    ▼               ▼               ▼               ▼
             ┌────────────┐ ┌─────────────┐ ┌──────────────┐ ┌─────────────┐
             │   Memory    │ │  Knowledge   │ │  Dynamic Tool │ │     RAG      │
             │    Node     │ │  Graph Node  │ │     Node      │ │    Node      │
             └────────────┘ └─────────────┘ └──────────────┘ └─────────────┘
                    │               │               │               │
             save/get user     entity-relation   live API call   vector search
             preferences        lookup (dict/     (e.g. wttr.in   over scraped
             (JSON store)       Neo4j-style)       weather API)    + chunked data
                    │               │               │               │
                    └───────────────┴───────────────┴───────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Final Response     │
                         └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python, FastAPI, Uvicorn |
| Orchestration | LangGraph (`StateGraph`) |
| Vector Store | ChromaDB |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Knowledge Graph | In-memory dictionary (triple store) |
| Memory Store | JSON file (`user_memory.json`) |
| Web Scraping | (BeautifulSoup, for data collection) |
| Dynamic Tool | wttr.in weather API via `requests` |

---

## Project Structure

```
memory augmented chat-bot/
├── app.py              # FastAPI entrypoint, exposes /chat endpoint
├── workflow.py         # LangGraph orchestration — routes queries to the right node
├── memory.py           # save_memory() / get_memory() — per-user persistent storage
├── rag.py               # rag_answer() — embedding + vector search + generation
├── graph.py             # graph_answer() — knowledge graph lookup
├── tools.py             # get_weather() — live weather API integration
├── data/
│   └── knowledge.txt    # source knowledge base for RAG
├── memory/
│   └── user_memory.json # persisted user memory store
└── requirements.txt
```

---

## Setup & Running

```bash
pip install fastapi uvicorn sentence-transformers chromadb requests langgraph
uvicorn app:app --reload
```

Once running, open the interactive API docs at:
```
http://127.0.0.1:8000/docs
```

Send queries via the `GET /chat?query=<your question>` endpoint.

---

## Sample Test Cases & Results

| # | Query | Routed To | Response |
|---|---|---|---|
| 1 | "My favorite language is Python" | Memory | "Okay, I will remember that your favorite language is Python." |
| 2 | "What is my favorite language?" | Memory | "Python" |
| 3 | "How is Python related to AI?" | Knowledge Graph | "Python is related to Artificial Intelligence" |
| 4 | "What is LangGraph used for?" | Knowledge Graph | "LangGraph is used for Workflow Orchestration" |
| 5 | "What is the weather in Delhi?" | Dynamic Tool | Live weather (e.g. "Delhi: 🌤 +37°C") |
| 6 | "What is the weather in Mumbai?" | Dynamic Tool | Live Mumbai weather |
| 7 | "What is Python used for?" | RAG | Answer generated from `knowledge.txt` |
| 8 | "Tell me a random fact about space" | RAG (fallback) | Closest semantic match from knowledge base — confirms graceful fallback with no crash on out-of-scope queries |

All 8 test cases were executed against the live server and returned expected results,
confirming the LangGraph router correctly dispatches each query type to the appropriate node.

---

## Evaluation

Manual evaluation was performed across the 8 test cases above, checking:

- **Context relevance** — did the routed node retrieve/use information relevant to the query?
- **Answer correctness** — did the final response match the expected/ground-truth answer?
- **Faithfulness** — was the response grounded in the retrieved data (no hallucination)?

All 8 cases passed on all three criteria. For out-of-scope queries (Test 8), the system
falls back to RAG's nearest semantic match rather than failing, demonstrating graceful
degradation.

---

## Known Limitations & Future Work

- **Knowledge Graph** is currently a small in-memory Python dictionary with a handful of
  hardcoded triples, intended to demonstrate the KG reasoning concept. A production version
  would use **Neo4j** with automated entity/relationship extraction (via NER or LLM-based
  triple extraction) for a dynamic, scalable graph.
- **Memory** currently stores a single preference type (favorite language) per user in a
  flat JSON file. This would extend naturally to a broader schema and a proper database
  (MongoDB/PostgreSQL) for multi-user, multi-attribute memory.
- **RAG knowledge base** is intentionally small for this submission; a larger scraped corpus
  would improve answer coverage and reduce reliance on the fallback path.
- **Dynamic Tools** currently integrates one live API (weather). Additional tools (news,
  search, etc.) can be added as new LangGraph nodes following the same pattern.
- **API endpoint** currently uses `GET /chat?query=...` for ease of manual testing via
  Swagger UI; a production deployment would use `POST /chat` with a JSON body to support
  richer inputs (conversation history, user_id, etc.).

---

## Author

Ayushi Tiwari — Celebal Excellence Intern
