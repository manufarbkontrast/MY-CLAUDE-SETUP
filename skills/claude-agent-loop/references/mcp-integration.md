# MCP Integration

## Connection Architecture

Two connection types, unified behind an abstract base class:

```
MCPConnection (ABC)
├── MCPConnectionStdio  → Local process (command + args)
└── MCPConnectionSSE    → Remote server (URL + headers)
```

## Connection Base Class

```python
from abc import ABC, abstractmethod
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

class MCPConnection(ABC):
    def __init__(self):
        self.session = None
        self._rw_ctx = None
        self._session_ctx = None

    @abstractmethod
    async def _create_rw_context(self):
        """Create read/write context based on connection type."""

    async def __aenter__(self):
        self._rw_ctx = await self._create_rw_context()
        read, write = await self._rw_ctx.__aenter__()
        self._session_ctx = ClientSession(read, write)
        self.session = await self._session_ctx.__aenter__()
        await self.session.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._session_ctx:
                await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)
            if self._rw_ctx:
                await self._rw_ctx.__aexit__(exc_type, exc_val, exc_tb)
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            self.session = None

    async def list_tools(self):
        return (await self.session.list_tools()).tools

    async def call_tool(self, tool_name, arguments):
        return await self.session.call_tool(tool_name, arguments=arguments)
```

## Stdio Connection

For local MCP servers running as a subprocess:

```python
class MCPConnectionStdio(MCPConnection):
    def __init__(self, command, args=None, env=None):
        super().__init__()
        self.command = command
        self.args = args or []
        self.env = env

    async def _create_rw_context(self):
        return stdio_client(
            StdioServerParameters(command=self.command, args=self.args, env=self.env)
        )
```

## SSE Connection

For remote MCP servers over HTTP:

```python
class MCPConnectionSSE(MCPConnection):
    def __init__(self, url, headers=None):
        super().__init__()
        self.url = url
        self.headers = headers or {}

    async def _create_rw_context(self):
        return sse_client(url=self.url, headers=self.headers)
```

## Factory Function

```python
def create_mcp_connection(config):
    conn_type = config.get("type", "stdio").lower()
    if conn_type == "stdio":
        return MCPConnectionStdio(
            command=config["command"],
            args=config.get("args"),
            env=config.get("env"),
        )
    elif conn_type == "sse":
        return MCPConnectionSSE(url=config["url"], headers=config.get("headers"))
    else:
        raise ValueError(f"Unsupported connection type: {conn_type}")
```

## Dynamic Tool Loading

Load all tools from all MCP servers at startup using `AsyncExitStack`:

```python
from contextlib import AsyncExitStack

async def setup_mcp_connections(mcp_servers, stack):
    if not mcp_servers:
        return []

    mcp_tools = []
    for config in mcp_servers:
        try:
            connection = create_mcp_connection(config)
            await stack.enter_async_context(connection)
            tool_definitions = await connection.list_tools()

            for tool_info in tool_definitions:
                mcp_tools.append(MCPTool(
                    name=tool_info.name,
                    description=tool_info.description or f"MCP tool: {tool_info.name}",
                    input_schema=tool_info.inputSchema,
                    connection=connection,
                ))
        except Exception as e:
            print(f"Error setting up MCP server {config}: {e}")

    return mcp_tools
```

**Why AsyncExitStack?** It manages the lifecycle of all connections. When the stack exits, all connections are properly cleaned up, even if one fails.

## Agent Integration

MCP tools are added to the agent's tool list temporarily during execution:

```python
async def run_async(self, user_input):
    async with AsyncExitStack() as stack:
        original_tools = list(self.tools)
        try:
            mcp_tools = await setup_mcp_connections(self.mcp_servers, stack)
            self.tools.extend(mcp_tools)
            return await self.agent_loop(user_input)
        finally:
            self.tools = original_tools  # Restore original tools
```

## Configuration Format

```python
mcp_servers = [
    {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    },
    {
        "type": "sse",
        "url": "http://localhost:3000/sse",
        "headers": {"Authorization": "Bearer token"},
    },
]
```
