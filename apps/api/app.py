from fastapi import FastAPI
from apps.api.routers import agent, health
from apps.domain.exceptions import NotFoundError
from fastapi import Request
from fastapi.responses import JSONResponse


app = FastAPI(
    title="Currency Exchange Agent",
    description="LangChain-powered currency exchange agent using OpenAI and ExchangeRate API",
    version="1.0.0",
)


@app.exception_handler(NotFoundError)
async def no_result_error_handler(_: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Currency Exchange Agent API",
        "description": "LangChain-powered currency exchange agent",
        "endpoints": {
            "POST /query": "Send currency exchange queries",
            "GET /health": "Health check endpoint",
        },
    }


app.include_router(health.router)
app.include_router(agent.router)
