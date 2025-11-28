import os
from typing import Annotated

from pydantic import Field
from pydantic_ai import Agent, FunctionToolset
from pydantic_ai.common_tools.tavily import tavily_search_tool
from pydantic_ai.mcp import MCPServerStdio, MCPServerStreamableHTTP

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4.1-mini")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
assert TAVILY_API_KEY

agent = Agent(
    f"openrouter:{OPENROUTER_MODEL}",
    output_type=Annotated[str, Field(max_length=2000)],  # pyright: ignore[reportArgumentType]
    system_prompt="The assistant name is Urara. Urara is an AI agent on Discord.",
    toolsets=[
        FunctionToolset([tavily_search_tool(TAVILY_API_KEY)]),
        MCPServerStreamableHTTP(
            "https://mcp.deepwiki.com/mcp",
            timeout=60,
            max_retries=5,
        ),
        MCPServerStdio(
            "uvx",
            ["kubernetes-mcp-server@latest", "--read-only", "--toolsets", "core"],
            timeout=60,
            max_retries=5,
        ),
    ],
)
