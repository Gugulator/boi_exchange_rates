import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BankOfIsraelAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "boi_exchange_rates"

PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Bank of Israel Exchange Rates component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Bank of Israel Exchange Rates from a config entry."""
    currencies = entry.options.get("currencies", [])
    hass.data[DOMAIN] = {"currencies": currencies}
    api = BankOfIsraelAPI(hass, DOMAIN)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="exchange_rate",
        update_method=api.get_exchange_rates,
        update_interval=timedelta(hours=3),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "currencies": currencies,
        "sensors": [],  # Initialize empty sensor list
    }

    entry.async_on_unload(entry.add_update_listener(update_listener))

    # Setup sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def update_listener(hass, entry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)