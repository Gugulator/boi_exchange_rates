"""Options flow for Bank of Israel Exchange Rates integration."""
from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import BankOfIsraelAPI
from .const import CONF_CURRENCIES, DOMAIN

_LOGGER = logging.getLogger(__name__)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for Bank of Israel Exchange Rates."""

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        api = BankOfIsraelAPI(async_get_clientsession(self.hass))
        available = await api.get_available_currencies()

        if not available:
            _LOGGER.warning("Could not fetch currency list from Bank of Israel API")

        current: list[str] = self.config_entry.options.get(CONF_CURRENCIES, [])

        schema = vol.Schema(
            {
                vol.Optional(CONF_CURRENCIES, default=current): cv.multi_select(
                    available
                )
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
