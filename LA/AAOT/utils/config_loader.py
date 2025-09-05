import json
import os

class ConfigLoader:

    def __init__(self):
        self.api_keys = {}
        self.settings = {}

    def load(self, config_dir="config"):
        api_keys_path = os.path.join(config_dir, "api_keys.json")
        if os.path.exists(api_keys_path):
            with open(api_keys_path, 'r') as f:
                self.api_keys = json.load(f)

        settings_path = os.path.join(config_dir, "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                self.settings = json.load(f)

    def has_api_key(self, service):
        if service in self.api_keys:
            key_data = self.api_keys[service]
            if isinstance(key_data, dict):
                return all(not val.startswith("YOUR_") and bool(val.strip()) for val in key_data.values())
            elif isinstance(key_data, str):
                return not key_data.startswith("YOUR_") and bool(key_data.strip())
        return False
