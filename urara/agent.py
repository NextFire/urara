import os

from pydantic import constr
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio, MCPServerStreamableHTTP

agent = Agent(
    f"openrouter:{os.getenv('OPENROUTER_MODEL', 'openai/gpt-4.1-mini')}",
    output_type=constr(max_length=2000),
    toolsets=[
        MCPServerStreamableHTTP("https://mcp.deepwiki.com/mcp", max_retries=5),
        MCPServerStdio(
            "uvx",
            ["kubernetes-mcp-server@latest", "--read-only", "--toolsets", "core"],
            max_retries=5,
        ),
    ],
)
