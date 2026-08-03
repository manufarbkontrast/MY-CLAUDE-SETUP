"""Minimal Claude agent with tool loop. ~40 lines, no dependencies beyond anthropic."""

import os
from anthropic import Anthropic


def run_agent(system: str, user_input: str, tools: list, tool_handlers: dict) -> str:
    """Run a minimal agent loop until Claude stops calling tools."""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": user_input}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            messages=messages,
            tools=tools,
        )

        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [b for b in response.content if b.type == "tool_use"]
        if not tool_calls:
            # Extract final text response
            return "\n".join(b.text for b in response.content if b.type == "text")

        tool_results = []
        for call in tool_calls:
            try:
                result = tool_handlers[call.name](**call.input)
            except Exception as e:
                result = f"Error: {e}"
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": call.id,
                "content": str(result),
            })
        messages.append({"role": "user", "content": tool_results})


# --- Example usage ---
if __name__ == "__main__":
    tools = [
        {
            "name": "calculate",
            "description": "Evaluate a math expression",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"],
            },
        }
    ]

    handlers = {
        "calculate": lambda expression: eval(expression),  # noqa: S307
    }

    result = run_agent(
        system="You are a helpful math assistant. Use the calculate tool.",
        user_input="What is 23 * 47 + 15?",
        tools=tools,
        tool_handlers=handlers,
    )
    print(result)
