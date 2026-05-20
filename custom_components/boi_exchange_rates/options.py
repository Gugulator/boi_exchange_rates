import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .api import BankOfIsraelAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "boi_exchange_rates"

CURRENCY_NAMES = {
    "USD": "US Dollar",
    "GBP": "British Pound",
    "JPY": "Japanese Yen 100 units",
    "EUR": "Euro",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "DKK": "Danish Krone",
    "NOK": "Norwegian Krone",
    "ZAR": "South African Rand",
    "SEK": "Swedish Krona",
    "CHF": "Swiss Franc",
    "JOD": "Jordanian Dinar",
    "LBP": "Lebanese Pound 10 units",
    "EGP": "Egyptian Pound",
}


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for Bank of Israel Exchange Rates integration."""

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        api = BankOfIsraelAPI(self.hass, DOMAIN)
        available_currencies = await api.get_available_currencies()

        sorted_currencies = sorted(
            [
                (CURRENCY_NAMES.get(code, code), code)
                for code in available_currencies.keys()
            ]
        )

        options_schema = vol.Schema(
            {
                vol.Optional(
                    "currencies",
                    default=list(self.config_entry.options.get("currencies", [])),
                ): cv.multi_select(
                    {code: f"{name} ({code})" for name, code in sorted_currencies}
                )
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
