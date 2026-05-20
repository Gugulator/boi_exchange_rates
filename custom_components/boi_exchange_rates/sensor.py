import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

CURRENCY_NAMES = {
    "USD": "US Dollar",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "EUR": "Euro",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "DKK": "Danish Krone",
    "NOK": "Norwegian Krone",
    "ZAR": "South African Rand",
    "SEK": "Swedish Krona",
    "CHF": "Swiss Franc",
    "JOD": "Jordanian Dinar",
    "LBP": "Lebanese Pound",
    "EGP": "Egyptian Pound",
}


class CurrencyRateSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing a currency exchange rate."""

    _attr_native_unit_of_measurement = "₪"
    _attr_icon = "mdi:currency-ils"

    def __init__(self, coordinator, currency: str) -> None:
        """Initialize the currency rate sensor."""
        super().__init__(coordinator)
        self._currency = currency
        currency_name = CURRENCY_NAMES.get(currency, currency)
        self._attr_name = f"Rate {currency_name}"
        # unique_id is required for HA to manage, update and remove entities properly
        self._attr_unique_id = f"{DOMAIN}_{currency.lower()}"

    @property
    def native_value(self):
        """Return the current exchange rate."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._currency)
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up the sensor platform."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    currencies = entry_data.get("currencies", [])

    sensors = [CurrencyRateSensor(coordinator, currency) for currency in currencies]
    async_add_entities(sensors, update_before_add=True)
