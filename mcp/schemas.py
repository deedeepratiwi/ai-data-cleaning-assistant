from pydantic import BaseModel
from typing import Dict, Any, List


class MCPRequest(BaseModel):
    tool: str
    payload: Dict[str, Any]


class MCPResponse(BaseModel):
    tool: str
    result: Dict[str, Any]


class ColumnStat(BaseModel):
    null_count: int
    dtype: str


class ProfilingResult(BaseModel):
    row_count: int
    column_stats: Dict[str, ColumnStat]


class Suggestion(BaseModel):
    operation: str
    params: Dict[str, Any]
