# mcsp/storage/chroma_vector_store.py
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class VectorStore:
    def __init__(self, persist_dir=".chroma_store"):
        self.client = chromadb.Client(chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir,
        ))
        self.embedding_func = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    def get_or_create_collection(self, name):
        return self.client.get_or_create_collection(name, embedding_function=self.embedding_func)

    def add(self, collection_name, doc_id, document):
        collection = self.get_or_create_collection(collection_name)
        collection.add(documents=[document], ids=[doc_id])

    def query(self, collection_name, query_text, top_k=5):
        collection = self.get_or_create_collection(collection_name)
        results = collection.query(query_texts=[query_text], n_results=top_k)
        return results["documents"]

    def persist(self):
        self.client.persist()
