"""Constants for Bank of Israel Exchange Rates integration."""

DOMAIN = "boi_exchange_rates"
PLATFORMS: list[str] = ["sensor"]

BASE_URL = "https://boi.org.il/PublicApi/GetExchangeRate?key="
ALL_RATES_URL = "https://boi.org.il/PublicApi/GetExchangeRates"

CONF_CURRENCIES = "currencies"
