from http import HTTPStatus
from fastapi import APIRouter
from fastapi import HTTPException
from apps.domain.models import QueryRequest, QueryResponse
from apps.domain.agents.currency_exchange import CurrencyExchangeAgent

currency_agent = CurrencyExchangeAgent()

router = APIRouter(
    tags=["agent"],
)


@router.post("/query", response_model=QueryResponse)
async def process_currency_query(request: QueryRequest):
    """
    Process currency exchange queries using the LangChain agent.

    This endpoint accepts natural language queries about currency exchange rates
    and returns responses from the OpenAI-powered agent with real-time data.

    Example queries:
    - "What's the current USD to EUR rate?"
    - "Show me exchange rates for British Pound"
    - "How much is 100 dollars in Japanese yen?"
    - "What are today's exchange rates?"
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Message cannot be empty")

        result = await currency_agent.process_query(request.message)

        if not result["success"]:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Agent processing failed: {result['error']}"
            )

        return QueryResponse(
            success=result["success"],
            response=result["response"],
            error=result["error"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")


@router.post("/query-sync", response_model=QueryResponse)
def process_currency_query_sync(request: QueryRequest):
    """
    Synchronous version of the currency query endpoint.

    This endpoint provides the same functionality as /query but processes
    requests synchronously, which might be useful for certain integrations.
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Message cannot be empty")

        result = currency_agent.process_query_sync(request.message)

        if not result["success"]:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Agent processing failed: {result['error']}"
            )

        return QueryResponse(
            success=result["success"],
            response=result["response"],
            error=result["error"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")
