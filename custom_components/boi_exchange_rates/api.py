"""API client for Bank of Israel Exchange Rates."""
from __future__ import annotations

import logging
import math

import aiohttp

from .const import ALL_RATES_URL, BASE_URL

_LOGGER = logging.getLogger(__name__)

# Abort requests that take longer than 10 seconds
_REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=10)


class BankOfIsraelAPI:
    """Client for the Bank of Israel public API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def get_exchange_rates(
        self, currencies: list[str]
    ) -> dict[str, float]:
        """Fetch exchange rates for the given list of currency codes."""
        rates: dict[str, float] = {}

        for currency in currencies:
            try:
                async with self._session.get(
                    BASE_URL + currency,
                    raise_for_status=True,
                    timeout=_REQUEST_TIMEOUT,
                ) as response:
                    # content_type=None skips MIME check since BOI API
                    # may return application/json without explicit header
                    data: dict = await response.json(content_type=None)
                    value = float(data["currentExchangeRate"])
                    if not math.isfinite(value):
                        _LOGGER.error(
                            "Non-finite exchange rate received for %s: %s",
                            currency,
                            value,
                        )
                        continue
                    rates[currency] = round(value, 2)
            except aiohttp.ClientError as err:
                _LOGGER.error("Error fetching rate for %s: %s", currency, err)
            except (ValueError, KeyError, TypeError):
                _LOGGER.error("Error parsing rate for %s", currency)

        return rates

    async def get_available_currencies(self) -> dict[str, str]:
        """Fetch all currencies available from Bank of Israel.

        Returns a dict of {code: code} sorted alphabetically,
        built entirely from the API response — no hardcoded names.
        """
        try:
            async with self._session.get(
                ALL_RATES_URL,
                raise_for_status=True,
                timeout=_REQUEST_TIMEOUT,
            ) as response:
                data: dict = await response.json(content_type=None)
                codes: list[str] = [
                    rate["key"]
                    for rate in data.get("exchangeRates", [])
                    if "key" in rate
                ]
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching available currencies: %s", err)
            return {}
        except (ValueError, KeyError, TypeError):
            _LOGGER.error("Error parsing available currencies")
            return {}

        return {code: code for code in sorted(codes)}
