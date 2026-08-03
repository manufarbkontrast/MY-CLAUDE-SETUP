"""Agent with MCP server integration. Connects to MCP servers and uses their tools."""

import asyncio
import os
from contextlib import AsyncExitStack
from typing import Any

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def connect_mcp_server(command: str, args: list[str], stack: AsyncExitStack):
    """Connect to an MCP server and return session + tool definitions."""
    server_params = StdioServerParameters(command=command, args=args)
    rw_ctx = stdio_client(server_params)
    read, write = await stack.enter_async_context(rw_ctx)
    session_ctx = ClientSession(read, write)
    session = await stack.enter_async_context(session_ctx)
    await session.initialize()

    tools_response = await session.list_tools()
    tool_defs = [
        {
            "name": t.name,
            "description": t.description or f"MCP tool: {t.name}",
            "input_schema": t.inputSchema,
        }
        for t in tools_response.tools
    ]
    return session, tool_defs


async def call_mcp_tool(session: ClientSession, name: str, arguments: dict) -> str:
    """Execute an MCP tool and return text result."""
    result = await session.call_tool(name, arguments=arguments)
    if hasattr(result, "content") and result.content:
        for item in result.content:
            if getattr(item, "type", None) == "text":
                return item.text
    return "No text content in tool response"


async def run_agent_with_mcp(
    system: str,
    user_input: str,
    mcp_servers: list[dict[str, Any]],
):
    """Run an agent loop with MCP tools."""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": user_input}]

    async with AsyncExitStack() as stack:
        # Connect to all MCP servers and collect tools
        all_tools = []
        tool_sessions = {}  # tool_name -> session

        for server_config in mcp_servers:
            session, tool_defs = await connect_mcp_server(
                command=server_config["command"],
                args=server_config.get("args", []),
                stack=stack,
            )
            for tool_def in tool_defs:
                all_tools.append(tool_def)
                tool_sessions[tool_def["name"]] = session

        print(f"Loaded {len(all_tools)} tools from {len(mcp_servers)} MCP servers")

        # Agent loop
        while True:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=system,
                messages=messages,
                tools=all_tools,
            )

            messages.append({"role": "assistant", "content": response.content})
            tool_calls = [b for b in response.content if b.type == "tool_use"]

            if not tool_calls:
                return "\n".join(b.text for b in response.content if b.type == "text")

            tool_results = []
            for call in tool_calls:
                try:
                    session = tool_sessions[call.name]
                    result = await call_mcp_tool(session, call.name, call.input)
                except Exception as e:
                    result = f"Error: {e}"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": str(result),
                })
            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    # Example: connect to a filesystem MCP server
    result = asyncio.run(run_agent_with_mcp(
        system="You are a helpful assistant with access to the filesystem.",
        user_input="List the files in /tmp",
        mcp_servers=[
            {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            },
        ],
    ))
    print(result)
