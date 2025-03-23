import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, USERNAME, PASSWORD, CITY_ID, CITY_NAME, UPDATE_INTERVAL
from .coordinator import McLautBalanceCheckerCoordinator
from .mclaut_api import McLautCredentials

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up integration from a config entry (UI flow or HACS install)."""
    try:
        credentials = McLautCredentials(
            username=entry.data.get(USERNAME),
            password=entry.data.get(PASSWORD),
            city_id=entry.data.get(CITY_ID),
            city_name=entry.data.get(CITY_NAME),
        )

        mclaut_coordinator = McLautBalanceCheckerCoordinator(
            hass, DOMAIN, UPDATE_INTERVAL, credentials
        )
        await mclaut_coordinator.async_config_entry_first_refresh()

        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = mclaut_coordinator

        await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
        return True
    except Exception as ex:
        _LOGGER.error("Unexpected error happened while set up the integration: %s", ex)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    status = await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
    if status:
        hass.data[DOMAIN].pop(entry.entry_id)
    return status
