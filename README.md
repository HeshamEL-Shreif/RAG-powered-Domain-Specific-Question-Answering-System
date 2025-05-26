# 📚 RAG-Powered Domain-Specific Question Answering System

An intelligent assistant that answers questions based on uploaded documents using **RAG (Retrieval-Augmented Generation)** powered by **LangChain** and **LLaMA 3.2 Instruct 1B**. The system features a sleek, interactive frontend built with **Dash**.

---

## 🚀 Demo

![Demo GIF](https://github.com/HeshamEL-Shreif/RAG-powered-Domain-Specific-Question-Answering-System/blob/main/demo.png)

---

## ✨ Features

- 📄 Upload multiple files (PDF, DOCX, CSV)
- 🔍 Chunk, embed, and index documents using LangChain
- 🤖 Ask natural language questions and get accurate answers from LLaMA 3
- 💬 Conversational interface with chat history via LangChain memory
- 🌐 Responsive UI built using Dash and Bootstrap

---

## 🧠 How It Works

1. **Upload Documents:** Users upload documents via the Dash frontend.
2. **Document Parsing & Chunking:** Files are parsed and split into text chunks using LangChain's document loaders and text splitters.
3. **Embedding + Indexing:** LangChain generates embeddings using `SentenceTransformers`, stores them in a Chroma vector store.
4. **Query Processing:** Users input natural language questions.
5. **Retrieval + Generation:** Relevant chunks are retrieved from Chroma and passed along with chat history to LLaMA 3.2 via a LangChain Runnable/Chain.
6. **Conversational Memory:** LangChain memory components maintain chat history for contextual answers.

---

## 🛠️ Tech Stack

| Component      | Tooling                                       |
|----------------|-----------------------------------------------|
| LLM            | `LLaMA 3.2 Instruct 1B` from Hugging Face     |
| Framework      | `LangChain` for RAG pipeline and memory       |
| Embeddings     | `SentenceTransformers`                        |
| Vector DB      | `Chroma` via LangChain                         |
| UI             | `Dash` and `Dash Bootstrap Components`        |

---

## 📁 Project Structure
```text
rag-pdf-assistant/
├── app/
│   ├── __init__.py
│   ├── data_handeler.py     # File parsing and text chunking logic, Embedding, Chroma store
│   ├── rag_pipeline.py      # LangChain RAG pipeline (retriever + generator + memory)
│
├── data/
│   ├── upload/
│   └── chroma_langchain_db/ # vector database
│
├── logger/
│   ├── __init__.py
│   └── logging_config.py    # Custom logging setup
│
├── logs/
│   ├── __init__.py
│   └── app.log              # Application log file
│
├── tests/                   # Unit tests for core components
│
├── ui/
│   ├── __init__.py
│   └── ui.py                # Dash frontend with file uploader + chat interface
│
├── demo.png                 # Static screenshot of the interface
├── main.py                  # Entry script to launch app
├── README.md                # Documentation
├── requirements.txt         # Dependencies
└── .gitignore
```


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
python main.py
```

## 📦 Requirements
- nltk 
- pypdf
- transformers
- dash
- dash-bootstrap-components
- dash-html-components
- torch
- numpy
- colorama
- dotenv
- langchain_community
- langchain_huggingface
- hf_xet
- langchain_chroma
