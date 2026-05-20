"""Config flow for Bank of Israel Exchange Rates integration."""
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN
from .options import OptionsFlowHandler


class BankOfIsraelFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Bank of Israel Exchange Rates integration."""

    VERSION = 1
    # CONNECTION_CLASS removed in HA 2022.x — use iot_class in manifest.json instead

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Bank of Israel Exchange Rates", data=user_input
            )

        return self.async_show_form(step_id="user")

    async def async_step_import(self, user_input=None):
        """Handle import from other integrations."""
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler()
