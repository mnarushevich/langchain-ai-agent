from typing import List, Dict, Any, Union
from langchain.agents import (
    create_openai_tools_agent,
    create_react_agent,
    AgentExecutor,
)
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from apps.domain.tools.currency_tool import CurrencyRateTool, SpecificCurrencyRateTool
from apps.api.config import settings


class CurrencyExchangeAgent:
    """LangChain agent for currency exchange queries using OpenAI or Ollama."""

    def __init__(self):
        """Initialize the currency exchange agent."""
        self.llm = self._create_llm()
        self.tools = self._create_tools()
        self.agent_executor = self._create_agent_executor()

    def _create_llm(self) -> Union[ChatOpenAI, ChatOllama]:
        """Create LLM instance based on configured provider."""
        if settings.model_provider.lower() == "ollama":
            print(f"Initializing Ollama model: {settings.model_name}")
            return ChatOllama(
                model=settings.model_name,
                base_url=settings.ollama_base_url,
                temperature=settings.model_temperature,
                num_predict=settings.model_max_tokens,
            )
        else:
            print(f"Initializing OpenAI model: {settings.model_name}")
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                model=settings.model_name,
                temperature=settings.model_temperature,
                max_tokens=settings.model_max_tokens,
            )

    def _create_tools(self) -> List:
        """Create and return the currency exchange tools."""
        return [CurrencyRateTool(), SpecificCurrencyRateTool()]

    def _create_agent_executor(self) -> AgentExecutor:
        """Create the agent executor with tools and prompt."""

        if settings.model_provider.lower() == "ollama":
            return self._create_react_agent_executor()
        else:
            return self._create_openai_tools_agent_executor()

    def _create_openai_tools_agent_executor(self) -> AgentExecutor:
        """Create OpenAI tools agent executor."""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""You are a helpful currency exchange assistant powered by {settings.model_provider.upper()} ({settings.model_name}). You have access to real-time currency exchange rates through specialized tools.

When users ask about currency rates or conversions:
1. Use the get_currency_rates tool to get general exchange rates for a base currency
2. Use the get_specific_currency_rate tool to get conversion rates between two specific currencies
3. Always provide the most current information available
4. Be helpful and explain the rates in a user-friendly way
5. If asked about trends or predictions, remind users that you only have current rates, not historical data or predictions

You can handle queries like:
- "What's the current USD to EUR rate?"
- "Show me exchange rates for GBP"
- "How much is 100 USD in Japanese Yen?"
- "What are the current exchange rates?"

Always be clear about when the rates were last updated and provide accurate, helpful information.""",
                ),
                ("user", "{input}"),
                (
                    "assistant",
                    "I'll help you with currency exchange information. Let me check the current rates for you.",
                ),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_openai_tools_agent(llm=self.llm, tools=self.tools, prompt=prompt)

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
        )

    def _create_react_agent_executor(self) -> AgentExecutor:
        """Create ReAct agent executor for Ollama models."""
        prompt_template = """You are a helpful currency exchange assistant. You have access to tools that provide real-time currency exchange rates.

TOOLS:
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT RULES:
1. You MUST use the available tools to get current exchange rates - do NOT provide rates from your training data
2. Always start by using the appropriate tool to get real-time data
3. For general rate queries, use get_currency_rates
4. For specific currency pair queries, use get_specific_currency_rate
5. Always provide the timestamp when rates were last updated
6. Be helpful and explain the rates clearly

Begin!

Question: {input}
Thought: I need to get current exchange rate information using the available tools.
{agent_scratchpad}"""

        prompt = ChatPromptTemplate.from_template(prompt_template)

        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=prompt)

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            return_intermediate_steps=True,
        )

    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query and return the response."""
        try:
            result = await self.agent_executor.ainvoke({"input": query})

            return {
                "success": True,
                "response": result.get("output", ""),
                "error": None,
            }

        except Exception as e:
            return {"success": False, "response": "", "error": str(e)}

    def process_query_sync(self, query: str) -> Dict[str, Any]:
        """Synchronous version of process_query."""
        try:
            result = self.agent_executor.invoke({"input": query})

            return {
                "success": True,
                "response": result.get("output", ""),
                "error": None,
            }

        except Exception as e:
            return {"success": False, "response": "", "error": str(e)}
