# Changelog

## [8.0.2] - 2026-05-21

### Changed
- Currency list in Options Flow is now built entirely from the API response — no hardcoded dictionary
- Sensor names now use currency codes directly (e.g. `Rate USD`, `Rate EUR`) instead of predefined English names
- If Bank of Israel adds or removes a currency, the integration will reflect that automatically without any code changes

### Removed
- `CURRENCY_NAMES` dictionary removed from `const.py`

---

## [8.0.1] - 2026-05-21

### Fixed
- Removing a currency checkbox in Options Flow now automatically deletes the corresponding sensor entity
- Previously the entity remained in the registry with a "no longer provided" warning and required manual deletion

---

## [8.0.0] - 2026-05-21

Complete rewrite for compatibility with current Home Assistant versions.

### Added
- `const.py` — centralized constants (domain, URLs, currency names)
- `translations/en.json` — English localization
- `translations/ru.json` — Russian localization
- `translations/he.json` — Hebrew localization
- `iot_class` field in `manifest.json` (required by modern HA)

### Changed
- Replaced `requests` with built-in Home Assistant `aiohttp` session (`async_get_clientsession`) — no more blocking calls
- `async_forward_entry_setup()` → `async_forward_entry_setups()` (plural, takes a list)
- `async_forward_entry_unload()` → `async_unload_platforms()`
- `state` / `unit_of_measurement` → `native_value` / `native_unit_of_measurement`
- Sensor now inherits from both `CoordinatorEntity` and `SensorEntity`
- `unique_id` added to each sensor entity — required for HA entity registry
- `OptionsFlowHandler` no longer accepts `config_entry` in `__init__` — HA now sets it automatically (fixes `AttributeError: property has no setter`)
- Removed `CONNECTION_CLASS` from config flow — replaced by `iot_class` in manifest
- `async_get_options_flow` now correctly decorated with `@staticmethod` and `@callback`
- Currency list in Options Flow is now fetched dynamically from the API
- Removed `async_setup()` — not needed for config entry based integrations

### Fixed
- `AttributeError: property 'config_entry' of 'OptionsFlowHandler' object has no setter`
- 500 Internal Server Error when opening integration options
- Blocking HTTP calls in the event loop
- Missing `unique_id` causing entities to not be tracked by HA entity registry
- `device_info` used as a string template conflicting with built-in HA property

---

## [7.0.0] - 2024-05-01

### Added
- Initial release
- Config Flow and Options Flow support
- DataUpdateCoordinator with 3-hour update interval
- Support for 14 currencies from Bank of Israel API
