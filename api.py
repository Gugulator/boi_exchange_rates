import logging

import aiohttp

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://boi.org.il/PublicApi/GetExchangeRate?key="
ALL_RATES_URL = "https://boi.org.il/PublicApi/GetExchangeRates"


class BankOfIsraelAPI:
    def __init__(self, hass, domain):
        self._hass = hass
        self._domain = domain

    async def get_exchange_rates(self) -> dict:
        """Fetch exchange rates for all configured currencies."""
        entry_data = self._hass.data[self._domain]
        # entry_data may be keyed by entry_id; find currencies
        currencies = None
        for value in entry_data.values():
            if isinstance(value, dict) and "currencies" in value:
                currencies = value["currencies"]
                break

        if not currencies:
            return {}

        exchange_rates = {}
        async with aiohttp.ClientSession() as session:
            for currency in currencies:
                try:
                    async with session.get(BASE_URL + currency) as response:
                        response.raise_for_status()
                        data = await response.json(content_type=None)
                        exchange_rates[currency] = round(
                            float(data["currentExchangeRate"]), 2
                        )
                except aiohttp.ClientError as err:
                    _LOGGER.error("Error fetching data for %s: %s", currency, err)
                except (ValueError, KeyError):
                    _LOGGER.error("Error parsing data for %s", currency)

        return exchange_rates

    async def get_available_currencies(self) -> dict:
        """Fetch the list of all currencies available from Bank of Israel."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ALL_RATES_URL) as response:
                    response.raise_for_status()
                    data = await response.json(content_type=None)
                    return {
                        rate["key"]: rate["key"]
                        for rate in data.get("exchangeRates", [])
                    }
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching available currencies: %s", err)
        except (ValueError, KeyError):
            _LOGGER.error("Error parsing available currencies")
        return {}
