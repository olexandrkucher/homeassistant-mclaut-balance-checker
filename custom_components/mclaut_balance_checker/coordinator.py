import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.mclaut_balance_checker.const import DOMAIN, UPDATE_INTERVAL
from custom_components.mclaut_balance_checker.mclaut_api import McLautApi, McLautCredentials

_LOGGER = logging.getLogger(__name__)



class McLautBalanceCheckerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, credential: McLautCredentials):
        super().__init__(
            hass=hass,
            name=DOMAIN,
            logger=_LOGGER,
            update_interval=timedelta(minutes=UPDATE_INTERVAL)
        )
        _LOGGER.info("McLautBalanceCheckerCoordinator init with data: %s", credential)
        self.mclaut_api = McLautApi(credential)

    async def _async_update_data(self):
        return self.mclaut_api.load_all_data()
