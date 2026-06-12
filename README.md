# 🤖 AI PDF Intelligence

AI PDF Intelligence is a Retrieval-Augmented Generation (RAG) powered PDF chatbot that allows users to upload PDF documents and interact with them using natural language. The application extracts document content, generates semantic embeddings, stores them in a vector database, and retrieves relevant context to provide accurate AI-generated answers.

## 🚀 Live Demo

https://ai-pdf-intelligence.streamlit.app

---

## ✨ Features

* 📄 Upload and analyze PDF documents
* 💬 Ask questions about document content
* 📝 Generate document summaries
* 🔍 Extract key insights and important information
* 🎯 Context-aware question answering using RAG
* 🧠 Semantic search with vector embeddings
* 📚 Conversation memory for follow-up questions
* 🎨 Modern responsive UI optimized for desktop and mobile
* ☁️ Deployed on Streamlit Cloud

---

## 🏗️ Architecture

```text
User Upload PDF
        │
        ▼
PDF Text Extraction
        │
        ▼
Text Chunking
        │
        ▼
Embedding Generation
        │
        ▼
Chroma Vector Database
        │
        ▼
Semantic Retrieval
        │
        ▼
Prompt Construction
        │
        ▼
OpenRouter LLM
        │
        ▼
AI Response
```

---

## ⚙️ Tech Stack

### Frontend

* Streamlit
* HTML/CSS

### Backend

* Python

### AI & RAG

* LangChain
* ChromaDB
* HuggingFace Embeddings
* OpenRouter API

### PDF Processing

* PyPDF

### Deployment

* Streamlit Community Cloud

---

## 🔄 Workflow

1. Upload a PDF document.
2. Extract text from the PDF.
3. Split text into manageable chunks.
4. Generate embeddings for each chunk.
5. Store embeddings in ChromaDB.
6. Retrieve relevant chunks for user queries.
7. Build a context-aware prompt.
8. Generate a response using the LLM.
9. Display the answer in a conversational interface.

---

## 📂 Project Structure

```text
AI PDF Chatbot/
│
├── app/
│   ├── core/
│   ├── services/
│   ├── state/
│   ├── ui/
│   ├── main.py
│   └── rag_pipeline.py
│
├── assets/
│   └── style.css
│
├── data/
│   └── pdfs/
│
├── requirements.txt
├── runtime.txt
└── .gitignore
```

---

## 🛠️ Installation

### Clone Repository

```bash
git clone https://github.com/Nandan0511/ai-pdf-intelligence.git
cd ai-pdf-intelligence
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

---

## ▶️ Run Locally

```bash
streamlit run app/main.py
```

---

## 📸 Use Cases

* Resume Analysis
* Research Paper Exploration
* Academic PDFs
* Business Reports
* Technical Documentation
* Policy Documents
* Project Reports

---

## 🎯 Challenges Solved

* Context-aware PDF question answering
* Efficient document retrieval
* Semantic search implementation
* Hallucination reduction through RAG
* Responsive Streamlit UI design
* Cloud deployment and configuration

---

## 🔮 Future Improvements

* OCR support for scanned PDFs
* Multi-PDF querying
* Source citations with page references
* PDF page-specific summaries
* Hybrid search (BM25 + Vector Search)
* Chat export functionality
* Multi-modal document understanding

---

## 👨‍💻 Author

**Nandan Patel**

* GitHub: https://github.com/Nandan0511
* LinkedIn: https://www.linkedin.com/in/nandan0601

---

## 📄 License

This project is open-source and available under the MIT License.
