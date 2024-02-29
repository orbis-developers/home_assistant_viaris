"""Control yaml file."""
import logging
import os

import yaml

_LOGGER = logging.getLogger(__name__)


class ConfigurationManager:
    "Class to control file."

    def __init__(self, serial) -> None:
        "Init configuration manager."
        self.file_path = os.path.join(
            "custom_components/viaris", "configuration_viaris.yaml"
        )
        self.serial_number = serial
        if not os.path.exists(self.file_path):
            _LOGGER.info("Creating new configuration file")
            initial_config = {"devices": {}}
            self.save_configuration(initial_config)

    def load_configuration(self):
        """Read YAML file."""
        config = {}

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                config = yaml.safe_load(file)
                if config["devices"] is None:
                    config["devices"] = {
                        self.serial_number: {"rt_frame": {"period": 3, "timeout": -1}}
                    }
                if self.serial_number not in config["devices"]:
                    config["devices"][self.serial_number] = {
                        "rt_frame": {"period": 3, "timeout": -1}
                    }
                    self.save_configuration(config)
        return config

    def save_configuration(self, config):
        """Save YAML file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file)
