# Core implementation for Retrieval-Augmented Generation (RAG)

from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader # Added for document loading
import json
import os
import nltk
from datetime import datetime

# Initialize NLTK (for advanced text processing if needed)
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download("punkt")


ENABLE_RAG = True  # Toggle for Retrieval-Augmented Generation
EMBEDDING_MODEL = "nomic-embed-text"  # Local embedding model compatible with Ollama
SAVE_HISTORY = True


def get_ollama_embeddings():
    """Initializes and returns the Ollama embeddings model."""
    return OllamaEmbeddings(model=EMBEDDING_MODEL)

def get_text_splitter(chunk_size=1000, chunk_overlap=200):
    """Creates and returns a text splitter for document chunking."""
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

class RAGCore:
    def __init__(self, embedding_model, text_splitter):
        self.embeddings = embedding_model
        self.text_splitter = text_splitter
        self.vector_store = {}
        print("RAG Core Initialized.")

    def add_document(self, doc_id, doc_content):
        """Processes and adds a document to the vector store."""
        chunks = self.text_splitter.split_text(doc_content)
        doc_vectors = self.embeddings.embed_documents(chunks)
        
        self.vector_store[doc_id] = {
            "chunks": chunks,
            "vectors": doc_vectors,
            "added_at": datetime.utcnow().isoformat()
        }
        print(f"Document '{doc_id}' added to vector store with {len(chunks)} chunks.")

    def load_documents_from_directory(self, directory_path, file_extensions=['.md', '.txt']):
        """Loads documents from a specified directory and adds them to the vector store."""
        if not os.path.isdir(directory_path):
            print(f"Error: Directory not found at {directory_path}")
            return

        print(f"Loading documents from {directory_path}...")
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if any(file_name.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.add_document(file_path, content)
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
        print("Document loading complete.")

    def retrieve(self, query, top_k=3):
        """Retrieves the most relevant document chunks for a given query."""
        if not self.vector_store:
            return []

        query_vector = self.embeddings.embed_query(query)
        
        # This is a simplified similarity search. 
        # A real implementation would use a proper vector database like FAISS or ChromaDB.
        all_chunks = []
        for doc_id, data in self.vector_store.items():
            for i, chunk_vector in enumerate(data["vectors"]):
                similarity = self._cosine_similarity(query_vector, chunk_vector)
                all_chunks.append({
                    "doc_id": doc_id,
                    "chunk_index": i,
                    "chunk_text": data["chunks"][i],
                    "similarity": similarity
                })
        
        # Sort by similarity and return top_k
        sorted_chunks = sorted(all_chunks, key=lambda x: x["similarity"], reverse=True)
        return sorted_chunks[:top_k]

    def _cosine_similarity(self, vec1, vec2):
        """Calculates cosine similarity between two vectors."""
        import numpy as np
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

# Example Usage (for testing)
if __name__ == "__main__":
    ollama_embed = get_ollama_embeddings()
    splitter = get_text_splitter()
    
    rag_system = RAGCore(ollama_embed, splitter)
    
    # Load documents from the Project_Tracker directory
    project_tracker_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Project_Tracker')
    rag_system.load_documents_from_directory(project_tracker_path)

    query = "What is the core vision of UGENTIC?"
    retrieved_chunks = rag_system.retrieve(query)
    
    print(f"\nQuery: {query}")
    print("Retrieved Chunks:")
    if retrieved_chunks:
        for chunk in retrieved_chunks:
            print(f"- (Similarity: {chunk['similarity']:.4f}) [Doc: {os.path.basename(chunk['doc_id'])}] {chunk['chunk_text']}")
    else:
        print("No relevant chunks retrieved.")

    query_hr = "How many vacation days are employees entitled to?"
    retrieved_hr_chunks = rag_system.retrieve(query_hr)

    print(f"\nQuery: {query_hr}")
    print("Retrieved HR Chunks:")
    if retrieved_hr_chunks:
        for chunk in retrieved_hr_chunks:
            print(f"- (Similarity: {chunk['similarity']:.4f}) [Doc: {os.path.basename(chunk['doc_id'])}] {chunk['chunk_text']}")
    else:
        print("No relevant chunks retrieved.")
