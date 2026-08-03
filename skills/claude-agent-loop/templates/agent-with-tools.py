"""Agent with custom tools using the dataclass-based Tool pattern."""

import asyncio
import os
from dataclasses import dataclass
from typing import Any

from anthropic import Anthropic


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "input_schema": self.input_schema}

    async def execute(self, **kwargs) -> str:
        raise NotImplementedError


# --- Define your custom tools ---

class ReadFileTool(Tool):
    def __init__(self):
        super().__init__(
            name="read_file",
            description="Read the contents of a file at the given path.",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"],
            },
        )

    async def execute(self, path: str) -> str:
        try:
            with open(path) as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found: {path}"
        except PermissionError:
            return f"Error: Permission denied: {path}"


class ListDirectoryTool(Tool):
    def __init__(self):
        super().__init__(
            name="list_directory",
            description="List files and directories at the given path.",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list"}
                },
                "required": ["path"],
            },
        )

    async def execute(self, path: str) -> str:
        import os as _os
        try:
            entries = _os.listdir(path)
            return "\n".join(sorted(entries))
        except FileNotFoundError:
            return f"Error: Directory not found: {path}"


# --- Agent with tool loop ---

async def run_agent(system: str, user_input: str, tools: list[Tool]) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": user_input}]
    tool_dict = {t.name: t for t in tools}

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            messages=messages,
            tools=[t.to_dict() for t in tools],
        )

        messages.append({"role": "assistant", "content": response.content})
        tool_calls = [b for b in response.content if b.type == "tool_use"]

        if not tool_calls:
            return "\n".join(b.text for b in response.content if b.type == "text")

        tool_results = []
        for call in tool_calls:
            try:
                result = await tool_dict[call.name].execute(**call.input)
            except KeyError:
                result = f"Error: Unknown tool '{call.name}'"
            except Exception as e:
                result = f"Error: {e}"
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": call.id,
                "content": str(result),
            })
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    result = asyncio.run(run_agent(
        system="You are a file system assistant. Use tools to explore files.",
        user_input="List the files in /tmp and read any .txt file you find.",
        tools=[ReadFileTool(), ListDirectoryTool()],
    ))
    print(result)
