# mcsp/storage/json_db_store.py
from tinydb import TinyDB, Query
from typing import Dict, List

class JSONStore:
    """
    A simple JSON-based key-value store for managing contexts.
    This class uses TinyDB to store contexts in a JSON file.
    """
    def __init__(self, path=".contexts.json"):
        self.db = TinyDB(path)
        self.contexts_table = self.db.table("contexts")

    def create_space(self, space: str):
        if not self.contexts_table.contains(Query().space == space):
            self.contexts_table.insert({"space": space, "contexts": []})

    def add_context(self, space: str, name: str):
        Context = Query()
        space_entry = self.contexts_table.get(Context.space == space)
        if space_entry and name not in space_entry["contexts"]:
            space_entry["contexts"].append(name)
            self.contexts_table.update({"contexts": space_entry["contexts"]}, Context.space == space)

    def get_spaces(self) -> List[str]:
        return [entry["space"] for entry in self.contexts_table.all()]

    def get_contexts(self, space: str) -> List[str]:
        Context = Query()
        entry = self.contexts_table.get(Context.space == space)
        return entry["contexts"] if entry else []

    def delete_context(self, space: str, name: str):
        Context = Query()
        entry = self.contexts_table.get(Context.space == space)
        if entry and name in entry["contexts"]:
            entry["contexts"].remove(name)
            self.contexts_table.update({"contexts": entry["contexts"]}, Context.space == space)

    def delete_space(self, space: str):
        self.contexts_table.remove(Query().space == space)
