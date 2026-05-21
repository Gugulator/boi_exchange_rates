"""Bank of Israel Exchange Rates integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BankOfIsraelAPI
from .const import CONF_CURRENCIES, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bank of Israel Exchange Rates from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    currencies: list[str] = entry.options.get(CONF_CURRENCIES, [])
    api = BankOfIsraelAPI(async_get_clientsession(hass))

    # Remove entities from the registry that are no longer selected
    entity_registry = async_get_entity_registry(hass)
    existing_entries = [
        entity
        for entity in entity_registry.entities.values()
        if entity.config_entry_id == entry.entry_id
    ]
    for entity_entry in existing_entries:
        # unique_id format: boi_exchange_rates_usd, boi_exchange_rates_eur, etc.
        currency_code = entity_entry.unique_id.replace(f"{DOMAIN}_", "").upper()
        if currency_code not in currencies:
            entity_registry.async_remove(entity_entry.entity_id)
            _LOGGER.debug("Removed entity for currency: %s", currency_code)

    async def _async_update_data() -> dict[str, float]:
        data = await api.get_exchange_rates(currencies)
        if not data and currencies:
            raise UpdateFailed("Failed to fetch any exchange rates")
        return data

    coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="exchange_rate",
        update_method=_async_update_data,
        update_interval=timedelta(hours=3),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "currencies": currencies,
        "api": api,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
