import collections
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "boi_exchange_rates"

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for Bank of Israel Exchange Rates integration."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        currency_names = {
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

        options_schema = vol.Schema(
    {
        vol.Optional(
            "currencies",
            default=list(self.config_entry.options.get("currencies", [])),
        ): cv.multi_select(
            {
                code: f"{name} ({code})"
                for code, name in sorted(
                    [
                        ("USD", "US Dollar"),
                        ("GBP", "British Pound"),
                        ("JPY", "Japanese Yen 100 units"),
                        ("EUR", "Euro"),
                        ("AUD", "Australian Dollar"),
                        ("CAD", "Canadian Dollar"),
                        ("DKK", "Danish Krone"),
                        ("NOK", "Norwegian Krone"),
                        ("ZAR", "South African Rand"),
                        ("SEK", "Swedish Krona"),
                        ("CHF", "Swiss Franc"),
                        ("JOD", "Jordanian Dinar"),
                        ("LBP", "Lebanese Pound 10 units"),
                        ("EGP", "Egyptian Pound"),
                    ]
                )
            }
        ),
    }
)

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            description_placeholders={
                "column1": "\n".join(
                    f"[ ] {name} ({code})" for code, name in sorted(
                        [
                            ("USD", "US Dollar"),
                            ("GBP", "British Pound"),
                            ("JPY", "Japanese Yen 100 units"),
                            ("EUR", "Euro"),
                            ("AUD", "Australian Dollar"),
                            ("CAD", "Canadian Dollar"),
                            ("DKK", "Danish Krone"),
                        ]
                    )
                ),
                "column2": "\n".join(
                    f"[ ] {name} ({code})" for code, name in sorted(
                        [
                            ("NOK", "Norwegian Krone"),
                            ("ZAR", "South African Rand"),
                            ("SEK", "Swedish Krona"),
                            ("CHF", "Swiss Franc"),
                            ("JOD", "Jordanian Dinar"),
                            ("LBP", "Lebanese Pound 10 units"),
                            ("EGP", "Egyptian Pound"),
                        ]
                    )
                ),
            },
        )
