import json
import logging
import os

import homeassistant.helpers.config_validation as cv
import voluptuous
from homeassistant import config_entries

from .const import DOMAIN, USERNAME, PASSWORD, CITY_ID, CITY_NAME
from .mclaut_api import City

CITY_UI_OPTION = "City"
PASSWORD_UI_OPTION = "Password"
USERNAME_UI_OPTION = "Username"
_LOGGER = logging.getLogger(__name__)


def load_cities_from_json() -> list[City]:
    path = os.path.join(os.path.dirname(__file__), "cities.json")
    with open(path, "r", encoding="utf-8") as f:
        city_dicts = json.load(f)
    return [City.from_dict(item) for item in city_dicts]


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My HACS App."""
    VERSION = 1

    def __init__(self):
        self._errors = {}
        self.city_options = load_cities_from_json()
        self.city_ui_options = {city.human_readable_city_name: city for city in self.city_options}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=voluptuous.Schema({
                    voluptuous.Required(USERNAME_UI_OPTION): cv.string,
                    voluptuous.Required(PASSWORD_UI_OPTION): cv.string,
                    voluptuous.Required(CITY_UI_OPTION): voluptuous.In(list(self.city_ui_options.keys()))
                }),
                errors=self._errors
            )

        username = user_input[USERNAME_UI_OPTION]
        city = self.city_ui_options[user_input[CITY_UI_OPTION]]
        _LOGGER.info('Integration setup started for user=%s in city=%s', username, city)

        return self.async_create_entry(
            title=username,
            data={
                USERNAME: username,
                PASSWORD: user_input[PASSWORD_UI_OPTION],
                CITY_ID: city.city_id,
                CITY_NAME: city.city_name
            }
        )
