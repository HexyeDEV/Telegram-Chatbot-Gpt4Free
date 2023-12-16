import chromadb
from chromadb.db.base import UniqueConstraintError


class Memory:
    def __init__(self, name):
        self.name = name
        self.client = chromadb.PersistentClient(
            path="./persist"
        )
        try:
            self.collection = self.client.create_collection(name)
        except UniqueConstraintError:
            self.collection = self.client.get_collection(name)
        except Exception as e:
            print(f"Error initializing Memory class: {e}")
            raise

    def insert(self, data, uuid):
        self.collection.add(documents=[data], ids=[uuid])

    def find(self, query):
        q = self.collection.query(query_texts=[query], n_results=2)
        return q["documents"]
