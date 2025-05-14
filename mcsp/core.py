# mcsp/core.py
from typing import Any, Dict, Union, List
from mcsp.stores.vector_store import VectorStore
from mcsp.stores.json_store import JSONStore


class ModelContextStore:
    def __init__(self):
        self.context_space_name = "model_contexts"
        self.context_space_description = "A space for storing model contexts"
        self.context_space_version = "1.0.0"
        self.context_space_author = "Your Name"
        self.context_space_author_email = "your.email@example.com"

        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.vector_store = VectorStore()
        self.db_store = JSONStore()

    def create_space(self, space_name: str, description: str = None):
        if not space_name:
            raise ValueError("Space name is required")
        if space_name in self.contexts:
            raise ValueError(f"Space '{space_name}' already exists")

        self.contexts[space_name] = {
            "description": description or self.context_space_description,
            "contexts": {},
        }

        # Save to persistence layers
        self.db_store.create_space(space_name)
        self.vector_store.create_space(space_name)
        self.db_store.add_context(space_name, space_name)
        self.vector_store.add(space_name, space_name, str(self.contexts[space_name]))
        return self.contexts[space_name]

    def get_space(self, space_name: str) -> Dict[str, Any]:
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")
        return self.contexts[space_name]

    def delete_space(self, space_name: str):
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")

        del self.contexts[space_name]
        self.db_store.delete_space(space_name)
        self.vector_store.delete_space(space_name)
        return f"Space '{space_name}' deleted"

    def get_version(self) -> str:
        return self.context_space_version

    def get_author(self) -> str:
        return self.context_space_author

    def get_author_email(self) -> str:
        return self.context_space_author_email

    def get_description(self) -> str:
        return self.context_space_description

    def set_description(self, description: str):
        self.context_space_description = description
        return f"Description set to: {description}"

    def set_version(self, version: str):
        self.context_space_version = version
        return f"Version set to: {version}"

    def set_author(self, author: str):
        self.context_space_author = author
        return f"Author set to: {author}"

    def set_author_email(self, email: str):
        self.context_space_author_email = email
        return f"Author email set to: {email}"

    def get_context(self, space_name: str, context_name: str) -> Any:
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")
        if context_name not in self.contexts[space_name]["contexts"]:
            raise ValueError(
                f"Context '{context_name}' does not exist in space '{space_name}'"
            )

        return self.contexts[space_name]["contexts"][context_name]

    def delete_context(self, space_name: str, context_name: str):
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")
        if context_name not in self.contexts[space_name]["contexts"]:
            raise ValueError(
                f"Context '{context_name}' does not exist in space '{space_name}'"
            )

        del self.contexts[space_name]["contexts"][context_name]
        self.db_store.delete_context(space_name, context_name)
        self.vector_store.delete_context(space_name, context_name)
        return f"Context '{context_name}' deleted from space '{space_name}'"

    def search_contexts(self, space_name: str, query: str) -> List[str]:
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")

        results = self.vector_store.query(space_name, query)
        return results["documents"] if results else []

    def search_all_spaces(self, query: str) -> List[str]:
        results = []
        for space_name in self.contexts:
            space_results = self.vector_store.query(space_name, query)
            if space_results:
                results.extend(space_results["documents"])
        return results

    def list_spaces(self) -> List[str]:
        return list(self.contexts.keys())

    def list_contexts(self, space_name: str) -> List[str]:
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")
        return list(self.contexts[space_name]["contexts"].keys())

    def clear_all(self):
        self.contexts.clear()
        self.db_store.db.drop_tables()
        self.vector_store.persist()
        return "All contexts cleared"

    def clear_context(self, space_name: str, context_name: str):
        if space_name not in self.contexts:
            raise ValueError(f"Space '{space_name}' does not exist")
        if context_name not in self.contexts[space_name]["contexts"]:
            raise ValueError(
                f"Context '{context_name}' does not exist in space '{space_name}'"
            )

        del self.contexts[space_name]["contexts"][context_name]
        self.db_store.delete_context(space_name, context_name)
        self.vector_store.delete_context(space_name, context_name)
        return f"Context '{context_name}' cleared from space '{space_name}'"
