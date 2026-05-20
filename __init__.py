import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import BankOfIsraelAPI

_LOGGER = logging.getLogger(__name__)

DOMAIN = "boi_exchange_rates"
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bank of Israel Exchange Rates from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    currencies = entry.options.get("currencies", [])
    api = BankOfIsraelAPI(hass, DOMAIN)

    # Store currencies so the API can read them during first refresh
    hass.data[DOMAIN][entry.entry_id] = {"currencies": currencies}

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="boi_exchange_rate",
        update_method=api.get_exchange_rates,
        update_interval=timedelta(hours=3),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "currencies": currencies,
    }

    entry.async_on_unload(entry.add_update_listener(update_listener))

    # Modern API: async_forward_entry_setups (plural) takes a list
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
