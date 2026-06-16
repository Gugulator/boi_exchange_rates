"""Sensor platform for Bank of Israel Exchange Rates."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bank of Israel Exchange Rate sensors."""
    entry_data: dict = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: DataUpdateCoordinator = entry_data["coordinator"]
    currencies: list[str] = entry_data["currencies"]

    async_add_entities(
        [CurrencyRateSensor(coordinator, currency) for currency in currencies],
        update_before_add=True,
    )


class CurrencyRateSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing a single currency exchange rate vs ILS."""

    _attr_native_unit_of_measurement = "₪"
    _attr_icon = "mdi:currency-ils"
    _attr_has_entity_name = False

    def __init__(
        self, coordinator: DataUpdateCoordinator, currency: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._currency = currency
        self._attr_name = f"Rate {currency}"
        self._attr_unique_id = f"{DOMAIN}_{currency.lower()}"

    @property
    def native_value(self) -> float | None:
        """Return the current exchange rate.

        Uses explicit None check so an empty dict {} is treated
        as valid data (no currencies selected) rather than falsy.
        """
        if self.coordinator.data is not None:
            return self.coordinator.data.get(self._currency)
        return None

    # CoordinatorEntity already implements _handle_coordinator_update
    # correctly, so no override is needed here.
