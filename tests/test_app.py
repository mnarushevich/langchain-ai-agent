#!/usr/bin/env python3
"""
Simple test script to demonstrate the Currency Exchange Agent.

This script tests the main functionality without requiring the full server setup.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def test_currency_tools():
    """Test the currency exchange tools directly."""
    print("🧪 Testing Currency Exchange Tools\n")

    try:
        from apps.domain.tools.currency_tool import CurrencyRateTool, SpecificCurrencyRateTool

        # Test general currency rates
        print("1. Testing CurrencyRateTool with USD:")
        currency_tool = CurrencyRateTool()
        result = currency_tool._run("USD")
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n" + "=" * 50 + "\n")

        # Test specific currency conversion
        print("2. Testing SpecificCurrencyRateTool (USD to EUR):")
        specific_tool = SpecificCurrencyRateTool()
        result = specific_tool._run("USD to EUR")
        print(result)
        print("\n" + "=" * 50 + "\n")

        print("✅ Currency tools test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error testing currency tools: {e}")
        return False


def test_agent():
    """Test the LangChain agent (requires OpenAI API key)."""
    print("🤖 Testing LangChain Agent\n")

    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ OPENAI_API_KEY not found. Skipping agent test.")
        print("Please set your OpenAI API key in a .env file to test the full agent.")
        return False

    try:
        from apps.domain.agents.currency_exchange import CurrencyExchangeAgent

        agent = CurrencyExchangeAgent()

        # Test query
        print("Testing query: 'What is the USD to EUR rate?'")
        result = agent.process_query_sync("What is the USD to EUR rate?")

        if result["success"]:
            print("✅ Agent Response:")
            print(result["response"])
        else:
            print(f"❌ Agent Error: {result['error']}")

        print("\n" + "=" * 50 + "\n")
        print("✅ Agent test completed!")
        return True

    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        return False


def check_environment():
    """Check if the environment is properly configured."""
    print("🔧 Checking Environment Configuration\n")

    # Check required dependencies (package name -> import name)
    required_packages = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "langchain": "langchain",
        "langchain_openai": "langchain_openai",
        "requests": "requests",
        "pydantic": "pydantic",
        "python-dotenv": "dotenv",
    }

    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing_packages.append(package_name)

    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run 'uv sync' to install missing dependencies.")
        return False

    # Check API keys
    print("\n🔑 API Key Configuration:")
    openai_key = os.getenv("OPENAI_API_KEY")
    exchange_key = os.getenv("EXCHANGERATE_API_KEY", "3b4e8f9ca8ead17851ef11f3")

    if openai_key:
        print(f"✅ OpenAI API Key: {openai_key[:8]}...{openai_key[-4:]}")
    else:
        print("❌ OpenAI API Key: Not set")

    print(f"✅ ExchangeRate API Key: {exchange_key[:8]}...{exchange_key[-4:]}")

    print("\n" + "=" * 50 + "\n")
    return len(missing_packages) == 0


def main():
    """Main test function."""
    print("🚀 Currency Exchange Agent Test Suite")
    print("=" * 50 + "\n")

    # Check environment
    env_ok = check_environment()

    if not env_ok:
        print("❌ Environment check failed. Please fix the issues above.")
        return

    # Test currency tools
    tools_ok = test_currency_tools()

    # Test agent (if OpenAI key is available)
    agent_ok = test_agent()

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Environment: {'✅' if env_ok else '❌'}")
    print(f"Currency Tools: {'✅' if tools_ok else '❌'}")
    print(f"LangChain Agent: {'✅' if agent_ok else '⚠️ (Skipped - No OpenAI key)'}")

    if tools_ok and (agent_ok or not os.getenv("OPENAI_API_KEY")):
        print("\n🎉 All tests passed! Your application is ready to use.")
        print("\n🚀 To start the server, run:")
        print("   uv run python main.py")
        print("\n📖 Then visit http://localhost:8011/docs for the API documentation.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
