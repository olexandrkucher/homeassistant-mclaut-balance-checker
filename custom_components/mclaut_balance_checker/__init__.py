from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from custom_components.mclaut_balance_checker.const import DOMAIN
from custom_components.mclaut_balance_checker.coordinator import McLautBalanceCheckerCoordinator


async def update_listener(hass, entry):
    """Handle options update."""
    coordinator: McLautBalanceCheckerCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_request_refresh()


async def async_setup(hass: HomeAssistant, entry: ConfigEntry):
    coordinator = McLautBalanceCheckerCoordinator(entry.data, hass)

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
