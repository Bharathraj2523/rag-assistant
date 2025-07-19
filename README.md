hey this personal rag-assistant

rag-assistant/                 ← Your project root folder
│
├── app.py                    ← 🖥️ Main Streamlit app — handles UI & user queries
├── rag_engine.py             ← 🧠 Backend logic — splits text, creates embeddings, retrieves answers
├── utils.py                  ← 🛠 Utility functions — reads PDFs, TXT files, saves uploads
├── requirements.txt          ← 📦 List of all required Python packages
├── .gitignore                ← 🙈 Prevents unwanted files (like venv) from going into Git
│
├── data/
│   └── uploaded_files/       ← 📂 Stores user-uploaded PDFs or TXT files temporarily
│
├── vector_store/
│   └── faiss_index/          ← 💾 Saves the FAISS vector DB index (text embeddings for search)
│
└── venv/                     ← 🧪 Your isolated Python environment (don’t touch this directly)
