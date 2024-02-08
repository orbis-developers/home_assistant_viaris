"""Definitions for viaris numbers MQTT."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant import config_entries
from homeassistant.components import mqtt
from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import UnitOfElectricCurrent
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.json import json_dumps
from homeassistant.util.json import json_loads

from . import ViarisEntityDescription
from .const import (
    CONF_SERIAL_NUMBER,
    CURRENT_LIMIT_CONN1_KEY,
    CURRENT_LIMIT_CONN2_KEY,
    MODEL_COMBIPLUS,
    STATE_CHARGING,
    STATE_CHARGING_POWER_LIMIT,
    STATE_PAUSED_CHARGING,
)
from .entity import ViarisEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class ViarisNumberEntityDescription(ViarisEntityDescription, NumberEntityDescription):
    """Number entity description for viaris."""

    domain: str = "number"


NUMBERS: tuple[ViarisNumberEntityDescription, ...] = (
    ViarisNumberEntityDescription(
        key=CURRENT_LIMIT_CONN1_KEY,
        name="Current limit connector 1",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_registry_enabled_default=True,
        disabled=False,
        native_min_value=6,
        mode=NumberMode.SLIDER,
        native_step=0.1,
    ),
    ViarisNumberEntityDescription(
        key=CURRENT_LIMIT_CONN2_KEY,
        name="Current limit connector 2",
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        entity_registry_enabled_default=True,
        disabled=False,
        native_min_value=6,
        mode=NumberMode.SLIDER,
        native_step=0.1,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Config entry setup."""

    async_add_entities(
        ViarisNumber(config_entry, description)
        for description in NUMBERS
        if not description.disabled
    )


class ViarisNumber(ViarisEntity, NumberEntity):
    """Representation of the Viaris portal."""

    entity_description: ViarisNumberEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: ViarisNumberEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description
        self._available = False  # Valor inicial de available
        self.serial_number = config_entry.data[CONF_SERIAL_NUMBER]
        self.current_value_conn1 = 0
        self.current_value_conn2 = 0
        self.max_value_lim = 32
        self.status_conn1 = 0
        self.status_conn2 = 0

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    def set_available(self, value):
        """Set value."""
        self._available = value

    @property
    def native_max_value(self) -> int:
        """Set max value."""
        return self.max_value_lim

    @property
    def native_value(self) -> int | None:
        """Return the value reported by the number."""
        if self.entity_description.key == CURRENT_LIMIT_CONN1_KEY:
            return self.current_value_conn1
        elif self.entity_description.key == CURRENT_LIMIT_CONN2_KEY:
            return self.current_value_conn2

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        message = json_dumps(
            {"idTrans": 1, "data": {"stat": {"ampacitySmCh": value * 1000}}}
        )
        if self.entity_description.key == CURRENT_LIMIT_CONN1_KEY:
            await mqtt.async_publish(
                self.hass,
                self._topic_set_current_conn1,
                message,
            )
            self.current_value_conn1 = value
        elif self.entity_description.key == CURRENT_LIMIT_CONN2_KEY:
            if self._model == MODEL_COMBIPLUS:
                await mqtt.async_publish(
                    self.hass,
                    self._topic_set_current_conn2,
                    message,
                )
            self.current_value_conn2 = value
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Add to hass."""

        @callback
        def mssg_received_rt(message):
            data = json_loads(message.payload)
            self.status_conn1 = data["data"]["elements"][0]["state"]
            self.status_conn2 = data["data"]["elements"][1]["state"]
            if self.entity_description.key == CURRENT_LIMIT_CONN1_KEY:
                if self.status_conn1 in (
                    STATE_CHARGING,
                    STATE_CHARGING_POWER_LIMIT,
                    STATE_PAUSED_CHARGING,
                ):
                    self.set_available(True)
                else:
                    self.set_available(False)
            elif self._model == MODEL_COMBIPLUS:
                if self.status_conn2 in (
                    STATE_CHARGING,
                    STATE_CHARGING_POWER_LIMIT,
                    STATE_PAUSED_CHARGING,
                ):
                    self.set_available(True)
                else:
                    self.set_available(False)
            else:
                self.set_available(False)

            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic_rt_subs, mssg_received_rt, 0)

    async def async_will_remove_from_hass(self) -> None:
        """Handle removal from Home Assistant."""
