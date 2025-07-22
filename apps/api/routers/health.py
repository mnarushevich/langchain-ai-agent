from fastapi import APIRouter

router = APIRouter(
    tags=["healthcheck"],
)


@router.get("/healthcheck", include_in_schema=True)
async def healthcheck() -> dict:
    return {"status": "alive"}
