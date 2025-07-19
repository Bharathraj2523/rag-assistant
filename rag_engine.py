# in this rag_engine.py file we will build the engine for the rag assistant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

#global variables
model = SentenceTransformer("all-MiniLM-L6-v2")
FAISS_INDEX_PATH = "vector_store/faiss_index/index.faiss"
CHUNKS_PATH = "vector_store/faiss_index/chunks.pkl"  # Renamed for clarity
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = genai.GenerativeModel(model_name="gemini-2.0-flash")

def chunk_text(text):
    '''
    this function chunk the text into smaller chunks
    Args:
        text: the text to chunk
    Returns:
        chunks: the chunks of the text
    '''
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_text(text)
    return chunks

def embed_chunk(chunks):
    '''
    this function embed the chunks
    Args:
        chunks: the chunks to embed
    Returns:
        embeddings: the embeddings of the chunks
    '''
    embeddings = model.encode(chunks)
    return embeddings

def create_vector_store(chunks):
    '''
    this function creates or updates the vector store by appending new chunks
    Args:
        chunks: the chunks to add to the vector store
    Returns:
        index: the updated FAISS index
    '''
    embeddings = embed_chunk(chunks)
    
    # Try to load existing index and chunks
    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            existing_chunks = pickle.load(f)
    except (FileNotFoundError, RuntimeError):
        # Create new index if none exists
        index = faiss.IndexFlatL2(embeddings.shape[1])
        existing_chunks = []
    
    # Add new chunks and embeddings
    updated_chunks = existing_chunks + chunks
    index.add(embeddings)
    
    save_vector_store(index, updated_chunks)
    return index

def save_vector_store(index, chunks):
    '''
    this function save the vector store
    Args:
        index: the index of the vector store
        chunks: all chunks (existing + new)
    Returns:
        None
    ''' 
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

def load_vector_store():
    '''
    this function load the vector store
    Args:
        None
    Returns:
        index: the index of the vector store
        chunks: all stored chunks
    '''
    try:
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks
    except (FileNotFoundError, RuntimeError):
        return None, []

def search_similar_chunks(query, k=3):
    '''
    Given a query, find top-k most similar chunks using FAISS.
    '''
    index, chunks = load_vector_store()
    if index is None or not chunks:
        return ["No documents processed yet. Please upload documents first."]
    
    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, k)

    results = [chunks[i] for i in indices[0]]
    return results

def generate_response(query):
    '''
    this function generate the response
    Args:
        query: the query to generate the response
    Returns:
        response: the response to the query
    '''
    results = search_similar_chunks(query)
    context = "\n".join(results)

    prompt = f"""You are a helpful assistant.
            Answer the following question based on the provided context.
            Context:
            {context}

            Question: {query}

            Answer:"""

    response = llm.generate_content(prompt)
    return response.text

def process_and_answer(query):
    return generate_response(query)