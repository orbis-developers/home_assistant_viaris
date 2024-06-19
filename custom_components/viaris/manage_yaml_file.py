"""Control yaml file."""
import asyncio
import logging
import os

import yaml

_LOGGER = logging.getLogger(__name__)


class ConfigurationManager:
    """Class to manage configuration file."""

    def __init__(self, serial_number)->None:
        """Initialize configuration manager."""
        self.file_path = os.path.join(
            "custom_components/viaris", "configuration_viaris.yaml"
        )
        self.serial_number = serial_number

    async def ensure_configuration_file(self):
        """Ensure the configuration file exists."""
        if not os.path.exists(self.file_path):
            _LOGGER.info("Creating new configuration file")
            initial_config = {"devices": {}}
            await self.save_configuration(initial_config)

    async def load_configuration(self):
        """Load YAML configuration file."""
        config = {}

        try:
            if os.path.exists(self.file_path):
                config = await asyncio.to_thread(self._read_yaml_file)
                if config["devices"] is None:
                    config["devices"] = {
                        self.serial_number: {"rt_frame": {"period": 3, "timeout": -1}}
                    }
                if self.serial_number not in config["devices"]:
                    config["devices"][self.serial_number] = {
                        "rt_frame": {"period": 3, "timeout": -1}
                    }
                    await self.save_configuration(config)
        except FileNotFoundError:
            _LOGGER.warning("Configuration file not found")
        except yaml.YAMLError as e:
            _LOGGER.error(f"Error loading YAML file: {e}")

        return config

    async def save_configuration(self, config):
        """Save YAML configuration file."""
        try:
            await asyncio.to_thread(self._write_yaml_file, config)
        except yaml.YAMLError as e:
            _LOGGER.error(f"Error saving YAML file: {e}")

    def _read_yaml_file(self):
        """Helper function to read YAML file."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _write_yaml_file(self, config):
        """Helper function to write YAML file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file)
