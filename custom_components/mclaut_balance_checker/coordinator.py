import logging
from datetime import timedelta
from typing import Any

import requests
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
        self.mclaut_api = McLautApi(credential, AsyncHttpClient(hass))

    async def _async_update_data(self):
        try:
            return await self.mclaut_api.load_all_data()
        except Exception as ex:
            _LOGGER.error("Error during update data: %s", ex)
            raise ex


class AsyncHttpClient:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def do_post(self, url: str, data, cookies) -> Any:
        return await self.hass.async_add_executor_job(self._do_post, url, data, cookies)

    @staticmethod
    def _do_post(url, data, cookies):
        response = requests.post(
            url=url,
            data=data,
            cookies=cookies,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Unexpected response for url: {url}, response: {response.status_code} - {response.reason}")
