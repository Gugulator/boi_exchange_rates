import logging

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

class CurrencyRateSensor(CoordinatorEntity):
    """Sensor representing a currency exchange rate."""

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

    def __init__(self, coordinator, currency):
        """Initialize the currency rate sensor."""
        super().__init__(coordinator)
        self._currency = currency

    @property
    def name(self):
        """Return the name of the sensor."""
        currency_name = self.CURRENCY_NAMES.get(self._currency, self._currency)
        return f"Rate {currency_name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._currency)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "₪"

    async def async_added_to_hass(self):
        """Register update callback."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    device_info = "Number of created entities: {}"

    async def async_update(self):
        """Update the sensor state."""
        self.device_info = self.device_info.format(len(self.coordinator.data))
        await super().async_update()

@callback
def async_get_sensors(hass, entry_id):
    """Get the sensors for the specified config entry."""
    entry_data = hass.data[DOMAIN][entry_id]
    coordinator = entry_data["coordinator"]
    currencies = entry_data["currencies"]

    sensors = []
    for currency in currencies:
        sensors.append(CurrencyRateSensor(coordinator, currency))

    return sensors

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    currencies = entry_data.get("currencies", [])

    # Remove sensors for removed currencies
    removed_currencies = set(entry_data.get("sensors", [])) - set(currencies)
    for currency in removed_currencies:
        sensor = next((s for s in entry_data["sensors"] if s.entity_id.endswith(currency)), None)
        if sensor:
            await sensor.async_remove()

    # Add new sensors for added currencies
    new_currencies = set(currencies) - set(s.entity_id.split("_")[-1] for s in entry_data.get("sensors", []))
    new_sensors = [CurrencyRateSensor(coordinator, currency) for currency in new_currencies]
    async_add_entities(new_sensors, True)

    # Update sensor list
    entry_data["sensors"] = [s for s in entry_data.get("sensors", []) if s.entity_id.split("_")[-1] in currencies]
    entry_data["sensors"].extend(new_sensors)
