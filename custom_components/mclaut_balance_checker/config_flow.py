import json
import logging
import os
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from custom_components.mclaut_balance_checker import McLautBalanceCheckerCoordinator, DOMAIN
from custom_components.mclaut_balance_checker.const import USERNAME, PASSWORD, CITY_NAME, CITY_ID
from custom_components.mclaut_balance_checker.mclaut_api import City

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from USER_SCHEMA with values provided by the user.
    """

    _LOGGER.info("validating input: %s", data)

    coordinator = McLautBalanceCheckerCoordinator(hass, data)
    # await coordinator.async_validate_input()

    return {"title": "McLaut Balance Checker"}


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
        if user_input is not None:
            _LOGGER.info("user_input: %s", user_input)

            selected_human_name = user_input[CITY_NAME]
            city = self.city_ui_options[selected_human_name]

            user_input[CITY_ID] = city.city_id
            user_input[CITY_NAME] = city.city_name

            return self.async_create_entry(title=user_input[USERNAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=voluptuous.Schema({
                voluptuous.Required(USERNAME): cv.string,
                voluptuous.Required(PASSWORD): cv.string,
                voluptuous.Required(CITY_NAME): voluptuous.In(list(self.city_ui_options.keys()))
            }),
            errors=self._errors
        )
