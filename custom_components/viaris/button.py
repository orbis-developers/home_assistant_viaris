"""Button support for viaris."""
from __future__ import annotations

import logging

from homeassistant import config_entries
from homeassistant.components import mqtt
from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.json import json_dumps

from . import ViarisEntityDescription
from .const import CONF_SERIAL_NUMBER
from .entity import ViarisEntity
from .manage_yaml_file import ConfigurationManager
from .number import numbers_buffer

_LOGGER = logging.getLogger(__name__)


class ViarisrButtonEntityDescription(ViarisEntityDescription, ButtonEntityDescription):
    """Button entity description for viaris."""

    domain: str = "button"
    payload_press: str = "true"


BUTTONS: tuple[ViarisrButtonEntityDescription, ...] = (
    ViarisrButtonEntityDescription(
        key="send_cfg_rt",
        name="Send rt config",
        device_class=ButtonDeviceClass.UPDATE,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""
    async_add_entities(
        ViarisButton(hass, config_entry, description)
        for description in BUTTONS
        if not description.disabled
    )


class ViarisButton(ViarisEntity, ButtonEntity):
    """Representation of viaris Button."""

    entity_description: ViarisrButtonEntityDescription

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        description: ViarisrButtonEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description
        super().__init__(config_entry, description)
        self.serial_number = config_entry.data[CONF_SERIAL_NUMBER]

    async def async_press(self) -> None:
        """Trigger the button action."""
        if self.serial_number in numbers_buffer:
            period_value = None
            timeout_value = None
            for entity in numbers_buffer[self.serial_number]:
                if entity.entity_id == f"number.{self.serial_number.lower()}_period_rt":
                    period_value = entity.state
                elif (
                    entity.entity_id
                    == f"number.{self.serial_number.lower()}_timeout_rt"
                ):
                    timeout_value = entity.state
            value = {
                "idTrans": 0,
                "data": {
                    "status": True,
                    "period": period_value,
                    "timeout": timeout_value,
                },
            }
            _LOGGER.info(value)
            value_json = json_dumps(value)
            mqtt.publish(self.hass, self._topic_rt_pub, value_json)
            config_manager = ConfigurationManager(self.serial_number)
            configuration = config_manager.load_configuration()
            configuration["devices"][self.serial_number]["rt_frame"][
                "period"
            ] = period_value
            configuration["devices"][self.serial_number]["rt_frame"][
                "timeout"
            ] = timeout_value
            config_manager.save_configuration(configuration)
        else:
            _LOGGER.warning(
                "No Viaris entity found for serial number: %s", self.serial_number
            )
