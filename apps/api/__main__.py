import uvicorn
from apps.api.config import settings


def main() -> None:
    """Startup event to initialize the application."""
    print("Currency Exchange Agent starting up...")
    print(f"Using ExchangeRate API: {settings.exchangerate_base_url}")
    print("Agent initialized successfully!")

    uvicorn.run("apps.api.app:app", host=settings.host, port=settings.port, reload=True)


if __name__ == "__main__":
    main()
