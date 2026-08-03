"""Template for creating a custom tool. Copy and adapt."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    """Base class - copy this into your project or import from your agent module."""
    name: str
    description: str
    input_schema: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "input_schema": self.input_schema}

    async def execute(self, **kwargs) -> str:
        raise NotImplementedError


# --- YOUR CUSTOM TOOL ---

class MyCustomTool(Tool):
    """Replace with your tool's purpose."""

    def __init__(self):
        super().__init__(
            name="my_tool",  # Must be unique across all tools
            description="Describe what this tool does clearly for the LLM.",
            input_schema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "What this parameter is for",
                    },
                    "param2": {
                        "type": "integer",
                        "description": "Optional numeric parameter",
                    },
                },
                "required": ["param1"],  # Only truly required params
            },
        )

    async def execute(self, param1: str, param2: int = 0) -> str:
        """Execute the tool. Return a string result."""
        # Your tool logic here
        result = f"Processed {param1} with value {param2}"
        return result


# --- TIPS ---
# 1. input_schema follows JSON Schema format
# 2. description is critical - the LLM uses it to decide when to call this tool
# 3. execute() receives **kwargs unpacked from the LLM's tool call input
# 4. Always return a string - the result goes back into the conversation
# 5. Handle errors gracefully - return error strings, don't raise
# 6. Keep tools focused on one thing - split complex operations
