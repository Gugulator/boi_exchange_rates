"""API client for Bank of Israel Exchange Rates."""
from __future__ import annotations

import logging

from aiohttp import ClientError, ClientSession

from .const import ALL_RATES_URL, BASE_URL

_LOGGER = logging.getLogger(__name__)


class BankOfIsraelAPI:
    """Client for the Bank of Israel public API."""

    def __init__(self, session: ClientSession) -> None:
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
                    BASE_URL + currency, raise_for_status=True
                ) as response:
                    data: dict = await response.json(content_type=None)
                    rates[currency] = round(float(data["currentExchangeRate"]), 2)
            except ClientError as err:
                _LOGGER.error("Error fetching rate for %s: %s", currency, err)
            except (ValueError, KeyError):
                _LOGGER.error("Error parsing rate for %s", currency)

        return rates

    async def get_available_currencies(self) -> dict[str, str]:
        """Fetch all currencies available from Bank of Israel.

        Returns a dict of {code: code} sorted alphabetically,
        built entirely from the API response — no hardcoded names.
        """
        try:
            async with self._session.get(
                ALL_RATES_URL, raise_for_status=True
            ) as response:
                data: dict = await response.json(content_type=None)
                codes: list[str] = [
                    rate["key"]
                    for rate in data.get("exchangeRates", [])
                    if "key" in rate
                ]
        except ClientError as err:
            _LOGGER.error("Error fetching available currencies: %s", err)
            return {}
        except (ValueError, KeyError):
            _LOGGER.error("Error parsing available currencies")
            return {}

        return {code: code for code in sorted(codes)}
