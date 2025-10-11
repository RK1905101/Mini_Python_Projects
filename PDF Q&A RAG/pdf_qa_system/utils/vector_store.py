import faiss
import numpy as np
from typing import List, Tuple
import pickle

class VectorStore:
    def __init__(self, embedding_generator):
        self.embedding_generator = embedding_generator
        self.index = None
        self.documents = []
        self.embeddings = []
        
        # Initialize FAISS index
        embedding_dim = embedding_generator.embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
    
    def add_documents(self, documents: List[str]):
        """Add documents to the vector store"""
        # Generate embeddings
        embeddings = self.embedding_generator.generate_embeddings(documents)
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store documents and embeddings
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
    
    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """Search for most similar documents and return with relevance scores"""
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        query_embedding = query_embedding.reshape(1, -1)
        
        # Search in FAISS
        distances, indices = self.index.search(query_embedding, k)
        
        # Return matching documents with scores
        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx != -1 and idx < len(self.documents):
                # Convert distance to similarity score (1 / (1 + distance))
                similarity = 1 / (1 + score)
                results.append((self.documents[idx], similarity))
        
        # Sort by similarity score in descending order
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Filter out low relevance results (optional)
        results = [(doc, score) for doc, score in results if score > 0.3]
        
        return results
    
    def save(self, path: str):
        """Save vector store to disk"""
        data = {
            'index': faiss.serialize_index(self.index),
            'documents': self.documents,
            'embeddings': self.embeddings
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, path: str):
        """Load vector store from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.index = faiss.deserialize_index(data['index'])
        self.documents = data['documents']
        self.embeddings = data['embeddings']