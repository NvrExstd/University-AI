from mcp.server.fastmcp import FastMCP

# Create an MCP server and give it a name
mcp = FastMCP("DemoServer")

# Define a simple tool: add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b