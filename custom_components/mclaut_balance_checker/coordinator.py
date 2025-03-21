import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, UPDATE_INTERVAL
from .http_client import AsyncHttpClient
from .mclaut_api import McLautApi, McLautCredentials

_LOGGER = logging.getLogger(__name__)


class McLautBalanceCheckerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, credentials: McLautCredentials):
        super().__init__(
            hass=hass,
            name=DOMAIN,
            logger=_LOGGER,
            update_interval=timedelta(minutes=UPDATE_INTERVAL)
        )
        self.mclaut_api = McLautApi(credentials, AsyncHttpClient(hass))

    async def _async_update_data(self):
        try:
            return await self.mclaut_api.load_all_data()
        except Exception as ex:
            _LOGGER.error("Error during update data: %s", ex)
            raise ex
