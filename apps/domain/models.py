from pydantic import BaseModel
from typing import Optional


# Pydantic models for request/response
class QueryRequest(BaseModel):
    """Request model for currency queries."""

    message: str

    class Config:
        json_schema_extra = {
            "example": {"message": "What's the current USD to EUR exchange rate?"}
        }


class QueryResponse(BaseModel):
    """Response model for currency queries."""

    success: bool
    response: str
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "The current USD to EUR exchange rate is 0.8599. This means 1 USD equals 0.8599 EUR. The rates were last updated on Mon, 21 Jul 2025 00:00:01 +0000.",
                "error": None,
            }
        }
