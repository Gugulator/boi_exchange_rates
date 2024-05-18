import requests
import logging

_LOGGER = logging.getLogger(__name__)

class BankOfIsraelAPI:
    def __init__(self, hass, domain):
        self._hass = hass
        self._domain = domain
        self._base_url = "https://boi.org.il/PublicApi/GetExchangeRate?key="

    async def get_exchange_rates(self):
        currencies = self._hass.data[self._domain]["currencies"]
        exchange_rates = {}

        for currency in currencies:
            try:
                response = await self._hass.async_add_executor_job(
                    requests.get, self._base_url + currency
                )
                response.raise_for_status()
                data = response.json()
                exchange_rates[currency] = round(float(data["currentExchangeRate"]), 2)
            except requests.exceptions.RequestException as err:
                _LOGGER.error(f"Error fetching data for {currency}: {err}")
            except (ValueError, KeyError):
                _LOGGER.error(f"Error parsing data for {currency}")

        return exchange_rates

    async def get_available_currencies(self):
        try:
            response = await self._hass.async_add_executor_job(
                requests.get, "https://boi.org.il/PublicApi/GetExchangeRates"
            )
            response.raise_for_status()
            data = response.json()
            return {rate["key"]: rate["key"] for rate in data["exchangeRates"]}
        except requests.exceptions.RequestException as err:
            _LOGGER.error(f"Error fetching available currencies: {err}")
            return {}
        except (ValueError, KeyError):
            _LOGGER.error("Error parsing available currencies")
            return {}