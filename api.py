import requests
import logging

RATES_URL = "https://boi.org.il/PublicApi/GetExchangeRates"
RATE_URL = "https://boi.org.il/PublicApi/GetExchangeRate?key="

_LOGGER = logging.getLogger(__name__)


class BankOfIsraelAPI:
    def __init__(self, hass, domain):
        self._hass = hass
        self._domain = domain

    async def get_exchange_rates(self) -> dict:
        currencies = self._hass.data[self._domain].get("currencies")
        exchange_rates = {}

        for currency in currencies:
            try:
                response = await self._hass.async_add_executor_job(requests.get, f'{RATE_URL}currency')
                response.raise_for_status()
                data = response.json()
                exchange_rates[currency] = round(float(data.get("currentExchangeRate")), 2)
            except requests.exceptions.RequestException as err:
                _LOGGER.error(f"Error fetching data for {currency}: {err}")
            except (ValueError, KeyError):
                _LOGGER.error(f"Error parsing data for {currency}")

        return exchange_rates

    async def get_available_currencies(self) -> dict:
        try:
            response = await self._hass.async_add_executor_job(requests.get, RATES_URL)
            response.raise_for_status()
            data = response.json()
            return {rate["key"]: rate["key"] for rate in data.get("exchangeRates")}
        except requests.exceptions.RequestException as err:
            _LOGGER.error(f"Error fetching available currencies: {err}")
            return {}
        except (ValueError, KeyError):
            _LOGGER.error("Error parsing available currencies")
            return {}
