import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from custom_components.mclaut_balance_checker import McLautBalanceCheckerCoordinator, DOMAIN
from custom_components.mclaut_balance_checker.const import USERNAME, PASSWORD, CITY_ID, CITY_NAME

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from USER_SCHEMA with values provided by the user.
    """

    _LOGGER.info("validating input: %s", data)

    coordinator = McLautBalanceCheckerCoordinator(hass, data)
    # await coordinator.async_validate_input()

    return {"title": "McLaut Balance Checker"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My HACS App."""

    VERSION = 1

    def __init__(self):
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            _LOGGER.info("user_input: %s", user_input)
            return

        return self.async_show_form(
            step_id="user",
            data_schema=voluptuous.Schema({
                voluptuous.Required(USERNAME): cv.string,
                voluptuous.Required(PASSWORD): cv.string,
                voluptuous.Required(CITY_ID): cv.positive_int,
                voluptuous.Required(CITY_NAME): cv.string,
            }),
            errors=self._errors
        )
