from fastapi import FastAPI, HTTPException

from mcp.schemas import MCPRequest, MCPResponse
from mcp.tools.profiling import run_profiling
from mcp.tools.suggestions import generate_suggestions
from mcp.tools.transformations import list_transformations

app = FastAPI(title="MCP Server")

TOOLS = {
    "profiling": run_profiling,
    "suggestions": generate_suggestions,
    "transformations": list_transformations,
}


@app.post("/mcp", response_model=MCPResponse)
def call_tool(req: MCPRequest):
    tool = TOOLS.get(req.tool)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    result = tool(req.payload)
    return MCPResponse(tool=req.tool, result=result)


@app.get("/health")
def health():
    return {"status": "ok"}
