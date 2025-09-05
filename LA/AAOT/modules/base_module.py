from abc import ABC, abstractmethod
import requests

class BaseModule(ABC):

    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__.replace('Module', '').lower()

    @abstractmethod
    def run(self, target):
        pass

    def make_request(self, url, method="GET", params=None, data=None, headers=None):
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=15)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, params=params, headers=headers, timeout=15)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if response.text.strip() else {}

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")
        except json.JSONDecodeError:
            raise ValueError("Failed to parse JSON response")
