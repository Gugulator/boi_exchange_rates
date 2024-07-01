# Bank of Israel Exchange Rates for Home Assistant

## Description

This integration for Home Assistant allows to get exchange rates from Bank of Israel and creates entities for chosen currency.

## Manual Installation

1. Create a directory named 'boi_exchange_rates' in your /homeassistant/custom_components/ folder.
2. Copy files from this repository to created directory.
3. Restart your Home Asssistant.
4. Go to Configuration -> Integrations.
5. Press "Add Integration" and search for "boi", you will get "Bank of Israel Exchange Rates" integration.
6. Press install. You're done.

## Configuration

1. Go to Configuration -> Integrations.
2. Choose this integration.
3. Choose currencies from dropdown menu.
4. Upon pressing "save" button integration will create entities for chosen currencies.
5. To delete entities, go to integration setting and uncheck unwanted currencies.

## Usage

Entities with chosen currencies will update values from Bank of Israel website every 3 hours.

## Contributors

- @Gugulator

## License

This project licensed by MIT License.
