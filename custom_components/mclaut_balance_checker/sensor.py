import logging
from _decimal import Decimal
from datetime import date, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, USERNAME, SENSORS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up the sensor platform."""
    entities = []
    coordinator = hass.data[DOMAIN][entry.entry_id]
    for description in SENSORS:
        entities.append(McLautSensor(entry, coordinator, description))
        _LOGGER.debug("Sensor created: %s", description)
    async_add_entities(entities)


class McLautSensor(SensorEntity):
    def __init__(self, entry, coordinator, description):
        super().__init__()
        self.coordinator = coordinator
        self.description = description

        username = entry.data.get(USERNAME)
        self._attr_icon = description["icon"]
        self._attr_name = f"{username} {description['name']}"
        self._attr_native_unit_of_measurement = description["unit"]
        self._attr_unique_id = f"{DOMAIN}_{username}_{description['key']}"

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the sensor's current value."""
        data = self.coordinator.data
        if data:
            return data.get(self.description["api_key"])
        return None
