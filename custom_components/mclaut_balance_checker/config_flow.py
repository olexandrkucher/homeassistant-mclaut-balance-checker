import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from custom_components.mclaut_balance_checker import McLautBalanceCheckerCoordinator, DOMAIN
from custom_components.mclaut_balance_checker.const import USERNAME, PASSWORD, CITY_ID, CITY_NAME

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = voluptuous.Schema({
    voluptuous.Required(USERNAME): cv.string,
    voluptuous.Required(PASSWORD): cv.string,
    voluptuous.Required(CITY_ID): cv.string,
    voluptuous.Required(CITY_NAME): cv.string,
})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from USER_SCHEMA with values provided by the user.
    """

    coordinator = McLautBalanceCheckerCoordinator(data, hass)
    # await coordinator.async_validate_input()

    return {"title": "McLaut Balance Checker"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=USER_SCHEMA,
                errors={}
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)

            await self.async_set_unique_id(user_input[USERNAME])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=info["title"], data=user_input)
        except ConnectionError:
            errors["base"] = "cannot_connect"
        except Exception as exception_error:  # pylint: disable=broad-except
            _LOGGER.exception(f"Unexpected exception {exception_error}")
            errors["base"] = "unknown"

        data_schema = self.add_suggested_values_to_schema(USER_SCHEMA, user_input)
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
