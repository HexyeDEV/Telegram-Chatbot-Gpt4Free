import chromadb


class Memory:
    def __init__(self, name):
        self.name = name
        try:
            self.client = chromadb.Client(
                chromadb.Settings(
                    chroma_db_impl="duckdb+parquet", persist_directory="./persist"
                )
            )
            self.collection = self.client.create_collection(name)
        except ValueError:
            self.collection = self.client.get_collection(name)
        except Exception as e:
            print(f"Error initializing Memory class: {e}")
            raise

    def insert(self, data, uuid):
        self.collection.add(documents=[data], ids=[uuid])

    def find(self, query):
        q = self.collection.query(query_texts=[query], n_results=2)
        return q["documents"]
