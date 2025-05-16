# 📚 RAG-Powered Domain-Specific Question Answering System

An intelligent assistant that answers questions based on uploaded documents using **RAG (Retrieval-Augmented Generation)** and **LLaMA 3 Instruct 1B**. This project leverages **Haystack** for the backend and **Dash** for a sleek, interactive frontend.

---

## 🚀 Demo

![Demo GIF](https://github.com/HeshamEL-Shreif/RAG-powered-Domain-Specific-Question-Answering-System/blob/main/image.png)

---

## ✨ Features

- 📄 Upload multiple files (PDF, DOCX, CSV)
- 🔍 Chunk, embed, and index documents using Haystack
- 🤖 Ask natural language questions and get accurate answers from LLaMA 3
- 💬 Chat-like interface with persistent conversation history
- 🌐 Clean UI built using Dash and Bootstrap

---

## 🧠 How It Works

1. **Upload Documents:** User uploads one or more documents via the Dash interface.
2. **Text Chunking:** Files are parsed and split into manageable text chunks.
3. **Embedding + Indexing:** Each chunk is embedded and stored in a FAISS vector database.
4. **Query Handling:** User enters a question.
5. **Retrieval + Generation:** Relevant chunks are retrieved using dense vector similarity, then passed to LLaMA 3 Instruct for answer generation.
6. **Conversation Memory:** Stores the chat history for follow-up context.

---

## 🛠️ Tech Stack

| Component      | Tooling                                      |
|----------------|----------------------------------------------|
| LLM            | `LLaMA 3 Instruct 1B` from Hugging Face      |
| Framework      | `Haystack` for document processing and RAG   |
| Embeddings     | `SentenceTransformers`     |
| Vector DB      | `FAISS`                                      |
| UI             | `Dash` and `Dash Bootstrap Components`       |
| Backend        | `FastAPI` (optional for scaling/deployment)  |

---

## 📁 Project Structure
rag-pdf-assistant/
├── app/                  # Backend logic
│   ├── rag_pipeline.py   # RAG pipeline using Haystack + FAISS
│   ├── retrieval.py      # Embedding and chunking logic
│   └── llm_response.py   # LLM integration (LLaMA 3)
│
├── ui/                   # Dash app
│   └── app.py            # Main frontend script
│
├── data/                 # Sample uploaded documents
├── tests/                # Unit/integration tests
├── README.md
├── requirements.txt
└── demo.mp4              # Short demo recording

---

## 🧪 Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/rag-pdf-assistant.git
cd rag-pdf-assistant
```
### 2. Install dependencies
``` bash
pip install -r requirements.txt
```
### 3. Run the app
``` bash
python ui/app.py
```

## 📦 Requirements
- Python 3.8+
- haystack
- transformers
- sentence-transformers or InstructorEmbedding
- dash, dash-bootstrap-components
- faiss-cpu or faiss-gpu
