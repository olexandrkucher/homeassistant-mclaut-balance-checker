import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.mclaut_balance_checker.const import DOMAIN, UPDATE_INTERVAL, USERNAME, PASSWORD, CITY_ID, \
    CITY_NAME
from custom_components.mclaut_balance_checker.mclaut_api import McLautApi

_LOGGER = logging.getLogger(__name__)

class McLautBalanceCheckerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, data: dict[str, Any], hass: HomeAssistant):
        super().__init__(
            hass=hass,
            name=DOMAIN,
            logger=_LOGGER,
            update_interval=timedelta(minutes=UPDATE_INTERVAL)
        )
        self.mclaut_api = McLautApi({
            USERNAME: data[USERNAME],
            PASSWORD: data[PASSWORD],
            CITY_ID: data[CITY_ID],
            CITY_NAME: data[CITY_NAME]
        })

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self._get_data)

    def _get_data(self) -> dict[str, Any]:
        return self.mclaut_api.load_all_data()
