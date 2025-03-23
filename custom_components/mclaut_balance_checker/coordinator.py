import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .http_client import AsyncHttpClient
from .mclaut_api import McLautApi, McLautCredentials

_LOGGER = logging.getLogger(__name__)


class McLautBalanceCheckerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(
        self,
        hass: HomeAssistant,
        domain: str,
        update_interval: timedelta,
        credentials: McLautCredentials,
    ):
        super().__init__(
            hass=hass,
            name=domain,
            logger=_LOGGER,
            update_interval=update_interval,
        )
        self.mclaut_api = McLautApi(credentials, AsyncHttpClient(hass))

    def __str__(self):
        return f"McLautBalanceCheckerCoordinator(domain={self.name}, update_interval={self.update_interval}, credentials={self.mclaut_api.credentials})"

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            _LOGGER.debug("Updating data for %s", self)
            return await self.mclaut_api.load_all_data()
        except Exception as ex:
            _LOGGER.error("Unexpected error happened while refreshing data: %s", ex)
            raise UpdateFailed(f"Update failed: {ex}")
