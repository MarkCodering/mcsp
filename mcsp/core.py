# mcsp/core.py
from typing import Dict, Any, List

class ModelContextStoreProtocol:
    def __init__(self, name, description, version, author, author_email, isTracking=False):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.author_email = author_email
        self.isTracking = isTracking
        self.store: Dict[str, Dict[str, Any]] = {}

    def create_space(self, space: str):
        if space not in self.store:
            self.store[space] = {}

    def create_context(self, space: str, name: str, context: Any):
        self.create_space(space)
        self.store[space][name] = context

    def get_context(self, space: str, name: str):
        return self.store.get(space, {}).get(name)

    def list_spaces(self) -> List[str]:
        return list(self.store.keys())

    def list_contexts(self, space: str) -> List[str]:
        return list(self.store.get(space, {}).keys())

    def delete_context(self, space: str, name: str):
        if space in self.store and name in self.store[space]:
            del self.store[space][name]

    def delete_space(self, space: str):
        self.store.pop(space, None)

    def search_contexts(self, space: str, query: str):
        return [
            ctx for name, ctx in self.store.get(space, {}).items()
            if query in str(ctx)
        ]

    def search_all_spaces(self, query: str):
        results = []
        for space in self.store:
            results.extend(self.search_contexts(space, query))
        return results

    def get_version(self):
        return self.version

    def get_author(self):
        return self.author

    def get_author_email(self):
        return self.author_email
