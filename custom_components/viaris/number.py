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
from homeassistant.const import UnitOfElectricCurrent, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.json import json_dumps
from homeassistant.util.json import json_loads

from . import ViarisEntityDescription
from .const import (
    CONF_SERIAL_NUMBER,
    CURRENT_LIMIT_CONN1_KEY,
    CURRENT_LIMIT_CONN2_KEY,
    MODEL_COMBIPLUS,
    PERIOD_RT_KEY,
    TIMEOUT_RT_KEY,
)
from .entity import ViarisEntity
from .manage_yaml_file import ConfigurationManager

_LOGGER = logging.getLogger(__name__)

numbers_buffer = {}


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
        # entity_registry_enabled_default=True,
        disabled=False,
        native_min_value=6,
        mode=NumberMode.SLIDER,
        native_step=0.1,
        translation_key="curr_lim_conn1",
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
        translation_key="curr_lim_conn2",
    ),
    ViarisNumberEntityDescription(
        key=PERIOD_RT_KEY,
        name="Rt frame period",
        device_class=NumberDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_registry_enabled_default=True,
        disabled=False,
        native_min_value=1,
        mode=NumberMode.BOX,
        native_step=1,
        translation_key="period_rt",
    ),
    ViarisNumberEntityDescription(
        key=TIMEOUT_RT_KEY,
        name="Rt frame timeout",
        device_class=NumberDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_registry_enabled_default=True,
        disabled=False,
        native_min_value=-1,
        mode=NumberMode.BOX,
        native_step=1,
        translation_key="timeout_rt",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Config entry setup."""
    entities = []
    for description in NUMBERS:
        if not description.disabled:
            entity = ViarisNumber(config_entry, description)
            entities.append(entity)
    async_add_entities(entities)
    numbers_buffer[config_entry.data[CONF_SERIAL_NUMBER]] = entities


class ViarisNumber(ViarisEntity, NumberEntity):
    """Representation of the Viaris."""

    entity_description: ViarisNumberEntityDescription

    def __init__(
        self,
        config_entry: config_entries.ConfigEntry,
        description: ViarisNumberEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, description)

        self.entity_description = description
        self._available = True  # Valor inicial de available
        self.serial_number = config_entry.data[CONF_SERIAL_NUMBER]
        self.current_value_conn1 = 0
        self.current_value_conn2 = 0
        self.max_value_lim = 32
        self.period_max = 1000
        self.timeout_max = 1000
        config_manager = ConfigurationManager(self.serial_number)
        configuration = config_manager.load_configuration()
        self.period = configuration["devices"][self.serial_number]["rt_frame"]["period"]
        self.timeout = configuration["devices"][self.serial_number]["rt_frame"][
            "timeout"
        ]

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
        if self.entity_description.key == PERIOD_RT_KEY:
            return self.period_max
        if self.entity_description.key == TIMEOUT_RT_KEY:
            return self.timeout_max
        return self.max_value_lim

    @property
    def native_value(self) -> int | None:
        """Return the value reported by the number."""
        if self.entity_description.key == CURRENT_LIMIT_CONN1_KEY:
            return self.current_value_conn1
        if self.entity_description.key == CURRENT_LIMIT_CONN2_KEY:
            return self.current_value_conn2
        if self.entity_description.key == PERIOD_RT_KEY:
            return self.period
        if self.entity_description.key == TIMEOUT_RT_KEY:
            return self.timeout

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
        elif self.entity_description.key == PERIOD_RT_KEY:
            self.period = value
        elif self.entity_description.key == TIMEOUT_RT_KEY:
            self.timeout = value

    async def async_added_to_hass(self):
        """Add to hass."""
        if self.entity_description.key in (PERIOD_RT_KEY, TIMEOUT_RT_KEY):
            self.set_available(True)

        @callback
        def mssg_received_rt(message):
            data = json_loads(message.payload)
            type_connector = data["data"]["elements"][1]["connectorName"]
            if type_connector in ("schuko", "schuko1", "schuko2"):
                if self.entity_description.key == CURRENT_LIMIT_CONN2_KEY:
                    self.set_available(False)
            self.async_write_ha_state()

        await mqtt.async_subscribe(self.hass, self._topic_rt_subs, mssg_received_rt, 0)

    async def async_will_remove_from_hass(self) -> None:
        """Handle removal from Home Assistant."""
