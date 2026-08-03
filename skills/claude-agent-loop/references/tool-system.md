# Tool System

## Tool Base Class

Simple dataclass pattern — minimal boilerplate:

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    async def execute(self, **kwargs) -> str:
        raise NotImplementedError("Subclasses must implement execute")
```

## Creating Custom Tools

Subclass `Tool` and implement `execute`:

```python
class ThinkTool(Tool):
    def __init__(self):
        super().__init__(
            name="think",
            description="Internal reasoning tool. Does not execute actions.",
            input_schema={
                "type": "object",
                "properties": {
                    "thought": {
                        "type": "string",
                        "description": "A thought to reason about.",
                    }
                },
                "required": ["thought"],
            },
        )

    async def execute(self, thought: str) -> str:
        return "Thinking complete!"
```

**Pattern**: `input_schema` follows JSON Schema format, matching the Claude API tool definition spec. The `**kwargs` in `execute` are unpacked from `call.input`.

## Parallel Tool Execution

Execute multiple tool calls concurrently using `asyncio.gather`:

```python
import asyncio

async def _execute_single_tool(call, tool_dict):
    response = {"type": "tool_result", "tool_use_id": call.id}
    try:
        result = await tool_dict[call.name].execute(**call.input)
        response["content"] = str(result)
    except KeyError:
        response["content"] = f"Tool '{call.name}' not found"
        response["is_error"] = True
    except Exception as e:
        response["content"] = f"Error executing tool: {str(e)}"
        response["is_error"] = True
    return response

async def execute_tools(tool_calls, tool_dict, parallel=True):
    if parallel:
        return await asyncio.gather(
            *[_execute_single_tool(call, tool_dict) for call in tool_calls]
        )
    else:
        return [await _execute_single_tool(call, tool_dict) for call in tool_calls]
```

**When to use sequential**: When tools have side effects that depend on each other (e.g., create file then read file).

## Error Handling

Each tool call is wrapped individually:
- `KeyError` → tool not found (reported as `is_error`)
- `Exception` → execution failed (reported as `is_error`)
- Success → result stringified and returned

The agent loop does **not** stop on tool errors. Claude receives the error message and can decide to retry or take a different approach.

## Tool Registration

Tools are registered at agent initialization and converted to a lookup dict in the loop:

```python
agent = Agent(
    name="my-agent",
    system="You are a helpful assistant.",
    tools=[ThinkTool(), FileReadTool(), WebSearchTool()],
)

# Inside agent_loop:
tool_dict = {tool.name: tool for tool in self.tools}
```

## MCP Tools

MCP tools follow the same `Tool` interface but delegate execution to an MCP server connection:

```python
class MCPTool(Tool):
    def __init__(self, name, description, input_schema, connection):
        super().__init__(name=name, description=description, input_schema=input_schema)
        self.connection = connection

    async def execute(self, **kwargs) -> str:
        try:
            result = await self.connection.call_tool(self.name, arguments=kwargs)
            if hasattr(result, "content") and result.content:
                for item in result.content:
                    if getattr(item, "type", None) == "text":
                        return item.text
            return "No text content in tool response"
        except Exception as e:
            return f"Error executing {self.name}: {e}"
```

This means native tools and MCP tools are interchangeable in the agent loop.
