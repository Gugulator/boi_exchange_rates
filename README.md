# Bank of Israel Exchange Rates for Home Assistant

![Version](https://img.shields.io/badge/version-8.0.0-blue)
![HACS](https://img.shields.io/badge/HACS-Custom-orange)
![License](https://img.shields.io/badge/license-MIT-green)

## Description

This custom integration for Home Assistant fetches official foreign currency exchange rates against the Israeli Shekel (ILS) from the [Bank of Israel public API](https://boi.org.il) and creates individual sensor entities for each selected currency.

## Features

- Fetches live exchange rates from the official Bank of Israel API
- Creates a separate sensor entity for each selected currency
- Sensors update automatically every 3 hours
- Add or remove currencies at any time via the integration options
- Fully configurable through the Home Assistant UI — no YAML required
- Compatible with HACS

## Supported Currencies

| Code | Currency |
|------|----------|
| USD  | US Dollar |
| EUR  | Euro |
| GBP  | British Pound |
| JPY  | Japanese Yen |
| AUD  | Australian Dollar |
| CAD  | Canadian Dollar |
| CHF  | Swiss Franc |
| DKK  | Danish Krone |
| NOK  | Norwegian Krone |
| SEK  | Swedish Krona |
| ZAR  | South African Rand |
| JOD  | Jordanian Dinar |
| LBP  | Lebanese Pound |
| EGP  | Egyptian Pound |

The list of available currencies is fetched dynamically from the API and may include additional currencies in the future.

## Installation

### Via HACS (Recommended)

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations**.
3. Click the three-dot menu in the top right and select **Custom repositories**.
4. Add `https://github.com/gugulator/boi_exchange_rates` with category **Integration**.
5. Find **Bank of Israel Exchange Rates** in the list and click **Download**.
6. Restart Home Assistant.

### Manual Installation

1. Download or clone this repository.
2. Copy the `boi_exchange_rates` folder into your `/config/custom_components/` directory.
3. Restart Home Assistant.

## Configuration

1. Go to **Settings → Devices & Services**.
2. Click **Add Integration** and search for `Bank of Israel`.
3. Select **Bank of Israel Exchange Rates** and click **Submit**.
4. After the integration is added, click **Configure**.
5. Select the currencies you want to track from the list.
6. Click **Submit** — sensor entities will be created automatically.

To remove a currency, go back to **Configure**, uncheck it and save.

## Entities

For each selected currency, a sensor entity is created:

| Entity ID | Friendly Name | Value | Unit |
|-----------|---------------|-------|------|
| `sensor.rate_us_dollar` | Rate US Dollar | 3.72 | ₪ |
| `sensor.rate_euro` | Rate Euro | 4.01 | ₪ |
| `sensor.rate_british_pound` | Rate British Pound | 4.67 | ₪ |

Values are rounded to two decimal places and updated every 3 hours.

## Example Automation

```yaml
automation:
  - alias: "Alert when USD rate rises above 4.00"
    trigger:
      - platform: numeric_state
        entity_id: sensor.rate_us_dollar
        above: 4.00
    action:
      - service: notify.mobile_app
        data:
          message: "USD rate is now {{ states('sensor.rate_us_dollar') }} ₪"
```

## Contributors

- [@Gugulator](https://github.com/gugulator)

## License

This project is licensed under the [MIT License](LICENSE).
