# mcsp/core.py
from typing import Any, Dict, Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcsp.store.vector_store import ChromaVectorStore
from mcsp.store.json_db_store import JSONDBStore

app = FastAPI()

class ModelContextStore:
    def __init__(self):
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.vector_store = ChromaVectorStore()
        self.db_store = JSONDBStore()

    def set_context(self, model_id: str, modality: str, context_data: Any):
        if not model_id or modality is None or context_data is None:
            raise ValueError("Model ID, modality, and context data are required")

        if model_id not in self.contexts:
            self.contexts[model_id] = {}

        self.contexts[model_id][modality] = context_data

        # Save to persistence layers
        self.db_store.create_space(model_id)
        self.db_store.add_context(model_id, modality)
        self.vector_store.add(model_id, f"{model_id}-{modality}", str(context_data))

    def get_context(self, model_id: str, modality: str = None) -> Union[Dict[str, Any], Any, None]:
        if model_id not in self.contexts:
            return None
        if modality:
            return self.contexts[model_id].get(modality)
        return self.contexts[model_id]

    def clear_context(self, model_id: str, modality: str = None):
        if model_id in self.contexts:
            if modality:
                self.contexts[model_id].pop(modality, None)
                self.db_store.delete_context(model_id, modality)
                if not self.contexts[model_id]:
                    del self.contexts[model_id]
                    self.db_store.delete_space(model_id)
            else:
                del self.contexts[model_id]
                self.db_store.delete_space(model_id)

    def clear_all(self):
        self.contexts.clear()
        self.db_store.db.drop_tables()
        self.vector_store.persist()

    def has_context(self, model_id: str, modality: str = None) -> bool:
        if modality:
            return model_id in self.contexts and modality in self.contexts[model_id]
        return model_id in self.contexts

    def list_spaces(self) -> List[str]:
        return self.db_store.get_spaces()

    def list_contexts(self, model_id: str) -> List[str]:
        return self.db_store.get_contexts(model_id)

    def search_contexts(self, model_id: str, query: str):
        return self.vector_store.query(model_id, query)