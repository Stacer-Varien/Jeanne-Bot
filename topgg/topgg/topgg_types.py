from typing import TypeVar

Key = TypeVar("Key")
Value = TypeVar("Value")


class JsonObject(dict[Key, Value]):
    import json as JSON

    def encode(self, indentation_level: int):
        return self.JSON.dumps(self, indent=indentation_level)
