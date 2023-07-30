"""
This module uses the Tautulli API to gather current stats from Plex
"""

import os
import logging
import requests
from dataclasses import dataclass, field
from typing import Union

logging.basicConfig(level=logging.DEBUG)

TAUTULLI_URL = os.getenv("TAUTULLI_URL")
TAUTULLI_API_KEY = os.getenv("TAUTULLI_API_KEY")

if not TAUTULLI_URL:
    raise EnvironmentError("Set the TAUTULLI_URL environment variable")

if not TAUTULLI_API_KEY:
    raise EnvironmentError("Set the TAUTULLI_API_KEY environment variable")


@dataclass
class PlexClient:
    """Class for api requests to Tautulli"""

    base_url: str = f"{TAUTULLI_URL}/api/v2?apikey={TAUTULLI_API_KEY}&cmd="
    headers: dict[str, str] = field(
        default_factory=lambda: ({"Content-type": "application/json"})
    )

    def get(self, uri: str) -> Union[dict, None]:
        """Get request, returns json if succesful, else null."""
        url = f"{self.base_url}{uri}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None


@dataclass
class Plex(PlexClient):
    def _validate_response(self, response: dict) -> bool:
        """Validate API response."""
        resp = response.get("response", {}) if response else {}
        return resp.get("result") == "success"

    def check_if_alive(self) -> bool:
        """Check if plex is alive."""
        response = self.get("server_status")
        if (
            self._validate_response(response)
            and response["response"]["data"]["connected"]
        ):
            logging.info(response)
            return True

        logging.error(
            f"Error connecting to Tautulli: {response['response']['message']}"
        )
        return False

    def get_activity(self) -> Union[dict, bool]:
        """Get current activity on Plex."""
        response = self.get("get_activity")
        if self._validate_response(response):
            logging.info(response)
            data = response["response"]["data"]
            return [
                str(data["stream_count"]),
                str(data["total_bandwidth"]),
                data["sessions"],
            ]
        logging.error(
            f"Error connecting to Tautulli: {response['response']['message']}"
        )
        return False

    def check_for_update(self) -> Union[bool, None]:
        """Check for any updates available on Plex."""
        response = self.get("get_pms_update")
        if self._validate_response(response):
            logging.info(response)
            return response["response"]["data"]["update_available"]
        logging.error(
            f"Error connecting to Tautulli: {response['response']['message']}"
        )
        return False


def main():
    plex = Plex()
    print("Plex alive status: ", plex.check_if_alive())
    print("Plex activity: ", plex.get_activity())
    print("Plex update status: ", plex.check_for_update())


if __name__ == "__main__":
    main()
