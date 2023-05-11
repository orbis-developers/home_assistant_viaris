"""Config flow for viaris integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_SERIAL_NUMBER,
    DEFAULT_NAME,
    DOMAIN,
    SERIAL_PREFIX_COMBI,
    SERIAL_PREFIX_UNI,
)

try:
    # < HA 2022.8.0
    from homeassistant.components.mqtt import MqttServiceInfo
except ImportError:
    # >= HA 2022.8.0
    from homeassistant.helpers.service_info.mqtt import MqttServiceInfo


_LOGGER = logging.getLogger(__name__)

# adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERIAL_NUMBER): str,
    }
)


class PlaceholderHub:
    """Placeholder class to make tests pass.

    Remove this placeholder class and replace with things from your PyPI package.

    """

    def __init__(self, serial_number: str) -> None:
        """Initialize."""
        self.serial_number = serial_number

    async def authenticate(self) -> bool:
        """Test if we can authenticate with the host."""
        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.

    """
    serial_number = data[CONF_SERIAL_NUMBER]

    hub = PlaceholderHub(serial_number)

    if not await hub.authenticate():
        raise CannotConnect

    if len(serial_number) != 13:
        raise WrongSerialLength

    if (str)(serial_number[5:13]).islower():
        raise InvalidSerial

    if (
        serial_number[0:5] == SERIAL_PREFIX_UNI
        or serial_number[0:5] == SERIAL_PREFIX_COMBI
    ):
        return {"title": f"{DEFAULT_NAME} {serial_number}"}
    raise InvalidSerial


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Viaris Connect."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize flow."""
        self._serial_number = None

    async def async_step_mqtt(self, discovery_info: MqttServiceInfo) -> FlowResult:
        """Handle a flow initialized by MQTT discovery."""
        subscribed_topic = discovery_info.subscribed_topic

        # Subscribed topic must be in sync with the manifest.json
        assert subscribed_topic == "XEO/VIARIS/#"

        topic = discovery_info.topic.split("/")
        self._serial_number = topic[5]
        if len(self._serial_number) == 13:
            if (
                self._serial_number[0:5] == SERIAL_PREFIX_UNI
                or self._serial_number[0:5] == SERIAL_PREFIX_COMBI
            ):
                await self.async_set_unique_id(self._serial_number)
                self._abort_if_unique_id_configured()
                return await self.async_step_discovery_confirm()
            else:
                return self.async_abort(reason="invalid_discovery_info")

        else:
            return self.async_abort(reason="invalid_discovery_info")

    async def async_step_discovery_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm the setup."""
        name = f"{DEFAULT_NAME} {self._serial_number}"
        self.context["title_placeholders"] = {"name": name}

        if user_input is not None:
            return self.async_create_entry(
                title=name,
                data={
                    CONF_SERIAL_NUMBER: self._serial_number,
                },
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders={"name": name, "serial": self._serial_number},
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except InvalidSerial:
            errors["base"] = "invalid_serial"
        except WrongSerialLength:
            errors["base"] = "invalid_serial_length"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(user_input[CONF_SERIAL_NUMBER])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class InvalidSerial(HomeAssistantError):
    """Error to indicate there is invalid prefix serial."""


class WrongSerialLength(HomeAssistantError):
    """Error to indicate there is invalid serial length."""
