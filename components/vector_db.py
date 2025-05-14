import faiss
import numpy as np
import pickle
import os

class FaissVectorDB:
    def __init__(self, dim=1024, index_path='files/faiss.index'):
        self.dim = dim
        self.index_path = index_path

        self.index = faiss.IndexFlatL2(dim)

        if os.path.exists(index_path):
            self.load()

    def upload(self, embeddings: np.ndarray):
        self.index.add(embeddings)

    def save(self):
        faiss.write_index(self.index, self.index_path)

    def load(self):
        self.index = faiss.read_index(self.index_path)

    def search(self, query_embedding: np.ndarray, top_k=3):
        D, I = self.index.search(query_embedding, top_k)
        return [{"index": int(i), "distance": float(d)} for i, d in zip(I[0], D[0]) if i != -1]
