from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import uvicorn
from typing import AsyncIterator, List, Union
import mcp.types as types
import anyio

# Initialize FastMCP with stateless HTTP (Streamable HTTP) support
mcp = FastMCP(
    name="mcp-streamable-http-stateless-demo",
    stateless_http=True,
)

# Define your tool implementations
@mcp.tool()
async def call_tool(
    name: str, arguments: dict
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    if name == "extract-wikipedia-article":
        return [
            types.TextContent(type="text", text="This is the article ...")
        ]

    ctx = mcp.request_context
    interval = arguments.get("interval", 1.0)
    count = arguments.get("count", 5)
    caller = arguments.get("caller", "unknown")

    for i in range(count):
        await ctx.session.send_log_message(
            level="info",
            data=f"Notification {i + 1}/{count} from caller: {caller}",
            logger="notification_stream",
            related_request_id=ctx.request_id,
        )
        if i < count - 1:
            await anyio.sleep(interval)

    return [
        types.TextContent(
            type="text",
            text=(
                f"Sent {count} notifications with {interval}s interval"
                f" for caller: {caller}"
            ),
        )
    ]

def home() -> FastAPI:
    return "server is running"
# Create FastAPI app and mount MCP Streamable HTTP transport and mount MCP Streamable HTTP transport
app = FastAPI()
# 3) Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

app.mount(
    "/mcp",
    mcp.streamable_http_app(),
)


# # Use MCP's lifespan context for startup/shutdown
# @app.on_event("startup")
# async def on_startup() -> None:
#     await mcp.session_manager.run().__aenter__()
#     mcp.logger.info("Application started with StreamableHTTP session manager!")

# @app.on_event("shutdown")
# async def on_shutdown() -> None:
#     await mcp.session_manager.run().__aexit__(None, None, None)
#     mcp.logger.info("Application shutting down...")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
