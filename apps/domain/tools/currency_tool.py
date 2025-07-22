import requests
from langchain.tools import BaseTool
from apps.api.config import settings


class CurrencyRateTool(BaseTool):
    """Tool for getting current currency exchange rates."""

    name: str = "get_currency_rates"
    description: str = (
        "Get current currency exchange rates. "
        "Input should be a base currency code (e.g., 'USD', 'EUR', 'GBP'). "
        "Returns exchange rates from the base currency to all other currencies."
    )

    def _run(self, base_currency: str = "USD") -> str:
        """Get currency exchange rates for the specified base currency."""
        try:
            # Clean and validate the base currency code
            base_currency = (
                base_currency.upper().strip().strip("'\"")
            )  # Remove quotes and whitespace

            # Construct the API URL
            url = f"{settings.exchangerate_base_url}/{settings.exchangerate_api_key}/latest/{base_currency}"

            # Make the API request
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Check if the API returned success
            if data.get("result") != "success":
                return f"Error: API returned result '{data.get('result')}'. Please check the currency code."

            # Format the response for better readability
            rates = data.get("conversion_rates", {})
            last_update = data.get("time_last_update_utc", "Unknown")

            # Create a formatted response
            result = f"Currency exchange rates (Base: {base_currency})\n"
            result += f"Last updated: {last_update}\n\n"

            # Add some key currencies first
            key_currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY"]

            result += "Major currencies:\n"
            for currency in key_currencies:
                if currency in rates and currency != base_currency:
                    result += f"{currency}: {rates[currency]:.4f}\n"

            # Add total count
            total_currencies = len(rates)
            result += f"\nTotal {total_currencies} currencies available."
            result += (
                "\nFor specific currency rates, you can ask about any currency code."
            )

            return result

        except requests.exceptions.RequestException as e:
            return f"Error fetching currency rates: {str(e)}"
        except Exception as e:
            return f"Error processing currency data: {str(e)}"

    async def _arun(self, base_currency: str = "USD") -> str:
        """Async version of the tool."""
        # For now, we'll use the sync version
        # In production, you might want to use aiohttp for async requests
        return self._run(base_currency)


class SpecificCurrencyRateTool(BaseTool):
    """Tool for getting specific currency conversion rates."""

    name: str = "get_specific_currency_rate"
    description: str = (
        "Get conversion rate between two specific currencies. "
        "Input should be in format 'FROM_CURRENCY to TO_CURRENCY' "
        "(e.g., 'USD to EUR', 'GBP to JPY'). Returns the conversion rate."
    )

    def _run(self, currency_pair: str) -> str:
        """Get conversion rate between two specific currencies."""
        try:
            # Parse the input and clean quotes
            currency_pair = currency_pair.strip().strip(
                "'\""
            )  # Remove quotes and whitespace
            parts = currency_pair.upper().replace(" TO ", " ").split()
            if len(parts) != 2:
                return "Error: Please provide currency pair in format 'FROM_CURRENCY to TO_CURRENCY'"

            from_currency, to_currency = parts[0], parts[1]

            # Get rates for the from_currency
            url = f"{settings.exchangerate_base_url}/{settings.exchangerate_api_key}/latest/{from_currency}"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("result") != "success":
                return f"Error: API returned result '{data.get('result')}'"

            rates = data.get("conversion_rates", {})

            if to_currency not in rates:
                return f"Error: Currency '{to_currency}' not found in exchange rates"

            rate = rates[to_currency]
            last_update = data.get("time_last_update_utc", "Unknown")

            result = f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}\n"
            result += f"Last updated: {last_update}"

            return result

        except requests.exceptions.RequestException as e:
            return f"Error fetching currency rates: {str(e)}"
        except Exception as e:
            return f"Error processing request: {str(e)}"

    async def _arun(self, currency_pair: str) -> str:
        """Async version of the tool."""
        return self._run(currency_pair)
