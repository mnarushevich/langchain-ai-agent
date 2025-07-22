# Currency Exchange Agent

A LangChain-powered currency exchange agent that supports both OpenAI and local Ollama models for natural language understanding, providing real-time currency conversion information through a FastAPI endpoint.

## Features

- 🤖 **Flexible LLM Support**: Switch between OpenAI GPT and local Ollama models
- 🏠 **Local AI Option**: Run completely offline with Ollama models (llama2, llama3, mistral, etc.)
- 💱 **Real-time Rates**: Uses ExchangeRate API for current currency exchange rates
- 🚀 **FastAPI**: Modern, fast web API with automatic documentation
- 🔧 **UV Project**: Uses UV for modern Python project management
- 📊 **Multiple Tools**: Supports general rates and specific currency conversions
- ⚙️ **Environment-Controlled**: Easy model switching via .env configuration
- 🏗️ **Modular Architecture**: Clean separation between API and domain logic

## Prerequisites

- Python 3.9+
- UV package manager
- **For OpenAI**: OpenAI API key
- **For Ollama**: Ollama installed locally (optional, for local AI)
- ExchangeRate API key (free tier available)

## Setup

### 1. Install UV (if not already installed)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd travel-agent

# Install dependencies
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Model Configuration
# Choose between "openai" or "ollama"
MODEL_PROVIDER=openai

# Model names:
# For OpenAI: gpt-3.5-turbo, gpt-4, gpt-4-turbo-preview, etc.
# For Ollama: llama2, llama3, mistral, codellama, etc.
MODEL_NAME=gpt-3.5-turbo

# Model parameters
MODEL_TEMPERATURE=0.1
MODEL_MAX_TOKENS=1000

# OpenAI API Key (required when MODEL_PROVIDER=openai)
OPENAI_API_KEY=your_openai_api_key_here

# Ollama Configuration (used when MODEL_PROVIDER=ollama)
OLLAMA_BASE_URL=http://localhost:11434

# ExchangeRate API Key (optional - has default)
EXCHANGERATE_API_KEY=3b4e8f9ca8ead17851ef11f3

# FastAPI Configuration (optional)
HOST=0.0.0.0
PORT=8000

# LangChain Configuration (optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

### 4. Setup Your AI Model

#### Option A: OpenAI (Cloud-based)

1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an account and generate an API key
3. Set `MODEL_PROVIDER=openai` in your `.env` file
4. Add your API key: `OPENAI_API_KEY=your_key_here`
5. Choose your model: `MODEL_NAME=gpt-3.5-turbo` (or gpt-4, etc.)

#### Option B: Ollama (Local/Offline)

1. **Install Ollama**:

   ```bash
   # On macOS
   brew install ollama

   # On Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # On Windows: Download from https://ollama.ai/download
   ```

2. **Pull a model**:

   ```bash
   # Start Ollama service
   ollama serve

   # In another terminal, pull a model
   ollama pull llama2        # or llama3, mistral, codellama, etc.
   ```

3. **Configure environment**:
   ```bash
   MODEL_PROVIDER=ollama
   MODEL_NAME=llama2         # or your chosen model
   OLLAMA_BASE_URL=http://localhost:11434
   ```

#### ExchangeRate API Key (Optional)

1. Visit [ExchangeRate API](https://www.exchangerate-api.com/)
2. Sign up for a free account (1,500 requests/month)
3. Get your API key from the dashboard
4. Add it to your `.env` file (or use the default provided)

## Running the Application

### Start the Server

```bash
# Using UV
uv run python -m apps.api

# Or activate the virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m apps.api
```

The server will start on `http://localhost:8011`

### Access the API Documentation

- **Swagger UI**: http://localhost:8011/docs
- **ReDoc**: http://localhost:8011/redoc

## API Endpoints

### POST /query

Send currency exchange queries using natural language.

**Request:**

```json
{
  "message": "What's the current USD to EUR exchange rate?"
}
```

**Response:**

```json
{
  "success": true,
  "response": "The current USD to EUR exchange rate is 0.8599. This means 1 USD equals 0.8599 EUR. The rates were last updated on Mon, 21 Jul 2025 00:00:01 +0000.",
  "error": null
}
```

### Example Queries

```bash
# Basic rate query
curl -X POST "http://localhost:8011/query" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the USD to EUR rate?"}'

# Multiple currencies
curl -X POST "http://localhost:8011/query" \
     -H "Content-Type: application/json" \
     -d '{"message": "Show me exchange rates for British Pound"}'

# Conversion calculation
curl -X POST "http://localhost:8011/query" \
     -H "Content-Type: application/json" \
     -d '{"message": "How much is 100 USD in Japanese Yen?"}'

# General rates
curl -X POST "http://localhost:8011/query" \
     -H "Content-Type: application/json" \
     -d '{"message": "What are the current exchange rates?"}'
```

### Other Endpoints

- **GET /**: API information and available endpoints
- **GET /health**: Health check endpoint
- **POST /query-sync**: Synchronous version of the query endpoint

## Project Structure

```
travel-agent/
├── pyproject.toml          # UV project configuration
├── README.md               # This file
├── .env                    # Environment variables (create this)
├── test_app.py             # Test script
├── uv.lock                 # UV lockfile
├── example_response.json   # Example API response
└── apps/                   # Application modules
    ├── api/                # FastAPI application
    │   ├── __init__.py
    │   ├── __main__.py     # Application entry point
    │   ├── app.py          # FastAPI app instance
    │   ├── config.py       # Configuration and settings
    │   └── routers/        # API route handlers
    │       ├── __init__.py
    │       ├── agent.py    # Currency agent endpoints
    │       └── health.py   # Health check endpoints
    └── domain/             # Business logic
        ├── __init__.py
        ├── models.py       # Pydantic models
        ├── exceptions.py   # Custom exceptions
        ├── agents/         # LangChain agents
        │   ├── __init__.py
        │   └── currency_exchange.py  # Currency agent implementation
        └── tools/          # LangChain tools
            ├── __init__.py
            └── currency_tool.py      # Currency API tools
```

## Available Currency Tools

### 1. CurrencyRateTool

- **Purpose**: Get general exchange rates for a base currency
- **Input**: Base currency code (e.g., "USD", "EUR", "GBP")
- **Output**: Formatted list of exchange rates

### 2. SpecificCurrencyRateTool

- **Purpose**: Get conversion rate between two specific currencies
- **Input**: Currency pair (e.g., "USD to EUR", "GBP to JPY")
- **Output**: Specific conversion rate with timestamp

## Development

### Run in Development Mode

```bash
# With auto-reload
uv run uvicorn apps.api.app:app --reload --host 0.0.0.0 --port 8011
```

### Code Formatting

```bash
# Format code with Black
uv run black .

# Lint with Ruff
uv run ruff check .
```

### Testing

```bash
# Run the test script
uv run python tests/test_app.py

# Run tests with pytest (when available)
uv run pytest
```

## Model Switching

You can easily switch between OpenAI and Ollama models by updating your `.env` file:

### Switch to OpenAI

```bash
MODEL_PROVIDER=openai
MODEL_NAME=gpt-3.5-turbo
OPENAI_API_KEY=your_openai_api_key_here
```

### Switch to Ollama (Local)

```bash
MODEL_PROVIDER=ollama
MODEL_NAME=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

### Popular Model Options

**OpenAI Models:**

- `gpt-3.5-turbo` - Fast and cost-effective
- `gpt-4` - More capable but slower
- `gpt-4-turbo-preview` - Latest GPT-4 variant

**Ollama Models:**

- `llama2` - Meta's Llama 2 model
- `llama3` - Latest Llama model
- `mistral` - Mistral AI's model
- `codellama` - Specialized for code understanding

### Benefits of Each Option

**OpenAI (Cloud):**

- ✅ High performance and accuracy
- ✅ No local setup required
- ✅ Always up-to-date
- ❌ Requires internet connection
- ❌ Usage costs

**Ollama (Local):**

- ✅ Completely offline
- ✅ No usage costs after setup
- ✅ Privacy (data stays local)
- ✅ Customizable
- ❌ Requires more system resources
- ❌ Initial setup time

## Usage Examples

The agent can handle various types of currency-related queries:

1. **Direct Rate Queries**:

   - "What's the USD to EUR rate?"
   - "How much is one dollar in euros?"

2. **General Rate Information**:

   - "Show me exchange rates for USD"
   - "What are the current rates?"

3. **Conversion Calculations**:

   - "Convert 100 USD to EUR"
   - "How much is 50 pounds in dollars?"

4. **Multiple Currency Information**:
   - "Show me rates for British Pound"
   - "What currencies can I convert to?"

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:

   - Ensure your API key is correctly set in the `.env` file
   - Check that your OpenAI account has sufficient credits
   - Verify `MODEL_PROVIDER=openai` is set

2. **Ollama Connection Issues**:

   - Ensure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`
   - Verify the base URL: `OLLAMA_BASE_URL=http://localhost:11434`
   - Try pulling the model again: `ollama pull llama2`

3. **Model Not Found**:

   - For OpenAI: Check if the model name is correct (e.g., `gpt-3.5-turbo`)
   - For Ollama: Ensure the model is pulled locally (`ollama pull model_name`)

4. **ExchangeRate API Issues**:

   - The default API key has limited requests
   - Sign up for a free account for more requests

5. **Import Errors**:

   - Run `uv sync` to ensure all dependencies are installed
   - Check that you're using the correct Python environment
   - Make sure `langchain-ollama` is installed for Ollama support

6. **Module Not Found Errors**:
   - Ensure you're running from the project root directory
   - The project uses absolute imports starting with `apps.`

### Debugging

Enable verbose logging by setting the environment variable:

```bash
export LANGCHAIN_VERBOSE=true
```

## Architecture Overview

The application follows a clean architecture pattern:

- **API Layer** (`apps/api/`): FastAPI application with routers and configuration
- **Domain Layer** (`apps/domain/`): Business logic including agents, tools, and models
- **Clear Separation**: API concerns are separated from business logic
- **Dependency Injection**: Configuration is injected into domain components

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request
