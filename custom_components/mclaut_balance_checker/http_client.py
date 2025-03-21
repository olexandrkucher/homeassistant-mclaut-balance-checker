import requests
from homeassistant.core import HomeAssistant


class AsyncHttpClient:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def do_post(self, url: str, data, cookies):
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
