import json
import logging
import os
from _decimal import Decimal
from datetime import date, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, USERNAME

_LOGGER = logging.getLogger(__name__)


def load_sensors_from_json() -> list[tuple]:
    path = os.path.join(os.path.dirname(__file__), "sensors.json")
    with open(path, "r", encoding="utf-8") as f:
        sensor_dicts = json.load(f)
    return sensor_dicts


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the sensor platform."""
    entities = []
    coordinator = hass.data[DOMAIN][entry.entry_id]
    for description in load_sensors_from_json():
        entities.append(McLautSensor(entry, coordinator, description))
        _LOGGER.debug('Sensor created: %s', description)
    async_add_entities(entities)


class McLautSensor(SensorEntity):
    def __init__(self, entry, coordinator, description):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.description = description

        self._attr_icon = description['icon']
        self._attr_name = f"{description['name']}"
        self._attr_native_unit_of_measurement = description['unit']
        self._attr_unique_id = f"{DOMAIN}_{entry.data.get(USERNAME)}_{description['key']}"

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the sensor's current value."""
        data = self.coordinator.data
        if data:
            return data.get(self.description['api_key'])
        return None
