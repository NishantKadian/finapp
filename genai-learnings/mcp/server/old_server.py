# File server.py

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from html2text import html2text

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount

from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from mcp.server.sse import SseServerTransport

# Create an MCP server instance with an identifier ("wiki")
mcp = FastMCP("wiki")

@mcp.tool()
def sum(x: float, y: float) -> float:
    """
    Sums two numbers.

    Usage:
        sum(1.0, 2.0)
    """
    try:
        print("entered the sum function")
        return x+y

    except Exception as e:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred: {str(e)}")) from e

sse = SseServerTransport("/messages/")

async def handle_sse(request: Request) -> None:
    _server = mcp._mcp_server
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send,
    ) as (reader, writer):
        await _server.run(reader, writer, _server.create_initialization_options())

from starlette.responses import PlainTextResponse

# …

app = Starlette(
    debug=True,
    routes=[
        Route("/", lambda req: PlainTextResponse("MCP server is running"), methods=["GET"]),
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)