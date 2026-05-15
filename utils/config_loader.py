# utils/config_loader.py
# Reads and provides access to config.yaml throughout the project

import yaml
import os


class ConfigLoader:
    """Loads and provides access to DualGuard configuration."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            # Automatically find config.yaml from anywhere in the project
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(root, "config", "config.yaml")

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Reads the YAML config file and returns it as a dictionary."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Config file not found at: {self.config_path}"
            )
        with open(self.config_path, "r") as f:
            raw = f.read()

        # Replace environment variable placeholders
        import re
        def replace_env(match):
            var_name = match.group(1)
            value = os.environ.get(var_name, "")
            return value

        raw = re.sub(r'\$\{(\w+)\}', replace_env, raw)
        config = yaml.safe_load(raw)

        if config is None:
            raise ValueError("Config file is empty.")
        return config

    def get_browserstack_credentials(self) -> dict:
        """Returns BrowserStack username and access key."""
        return self.config.get("browserstack", {})

    def get_device_config(self, locale: str) -> dict:
        """
        Returns device configuration for a given locale.
        locale: 'english' or 'arabic'
        """
        devices = self.config.get("devices", {})
        if locale not in devices:
            raise KeyError(
                f"Locale '{locale}' not found in config. "
                f"Available: {list(devices.keys())}"
            )
        return devices[locale]

    def get_app_config(self) -> dict:
        """Returns app configuration."""
        return self.config.get("app", {})

    def get_test_config(self) -> dict:
        """Returns test settings like timeout and directories."""
        return self.config.get("test", {})

    def get_reporting_config(self) -> dict:
        """Returns reporting configuration."""
        return self.config.get("reporting", {})


# Single instance used across the entire project
config = ConfigLoader()