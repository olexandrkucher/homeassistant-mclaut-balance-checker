import logging

from homeassistant.const import Platform

from custom_components.mclaut_balance_checker.const import DOMAIN, USERNAME, PASSWORD, CITY_ID, CITY_NAME
from custom_components.mclaut_balance_checker.coordinator import McLautBalanceCheckerCoordinator
from .mclaut_api import McLautCredentials

_LOGGER = logging.getLogger(__name__)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration from configuration.yaml (optional)."""
    return True  # or False if you want to block YAML-only setup


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from a config entry (UI flow or HACS install)."""
    credentials = McLautCredentials(
        username=entry.data.get("username"),
        password=entry.data.get("password"),
        city_id=entry.data.get("city_id"),
        city_name=entry.data.get("city_name")
    )

    coordinator = McLautBalanceCheckerCoordinator(hass, credentials)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
