import faiss
import pickle
import os
import numpy as np


class Memory:
    def __init__(self, name, dim=512):
        self.name = name
        self.dim = dim
        self.index_path = f"./persist/{name}.faiss"
        self.data_path = f"./persist/{name}_data.pkl"
        self.index = faiss.IndexFlatL2(dim)
        self.data = {}
        
        if not os.path.exists("./persist"):
            os.makedirs("./persist")
        
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.data_path):
            with open(self.data_path, "rb") as f:
                self.data = pickle.load(f)

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.data_path, "wb") as f:
            pickle.dump(self.data, f)

    def insert(self, data, uuid):
        if uuid in self.data:
            return  # Avoid duplicate entries
        
        self.data[uuid] = data
        vector = np.random.rand(512)
        vector = np.array([vector], dtype=np.float32)
        if self.index.is_trained:
            self.index.add(vector)
        else:
            self.index.train(vector)
            self.index.add(vector)
        self._save_index()

    def find(self, query_vector, n_results=2):
        if self.index.ntotal == 0:
            return []
        
        query_vector = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_vector, n_results)
        results = []
        for i, distance in zip(indices[0], distances[0]):
            if i in self.data:
                results.append((self.data[i], distance))
        return results
