import logging
from typing import Mapping, Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import McLautBalanceCheckerCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: McLautBalanceCheckerCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            McLautSensor(entry, coordinator)
            for warehouse in coordinator.warehouses
        ]
    )

class McLautSensor(SensorEntity):
    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: McLautBalanceCheckerCoordinator
    ) -> None:
        super().__init__(coordinator)

        self.entity_description = SensorEntityDescription(
            key=f"mclaut_sensor",
            name=f"McLaut Balance Checker",
            state_class=SensorStateClass.TOTAL,
            icon="mdi:package-down",
        )
        self._attr_unique_id = "-".join([
            entry.entry_id,
            self.entity_description.key,
        ])
        self._attr_device_info = DeviceInfo(
            name=entry.title,
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry.entry_id)}
        )

    # def native_value(self) -> StateType | date | datetime | Decimal:
    #     return super().native_value()

    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {
            'balance': '123',
            'phone': '+380123456789',
        }
