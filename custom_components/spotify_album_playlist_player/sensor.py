# custom_components/spotify_album_playlist_player/sensor.py
import logging
import requests
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.config_entry import ConfigEntry
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "spotify_album_playlist_player"

class SpotifyLibraryTypeSensor(SensorEntity):
    def __init__(self, name: str, unique_id: str,
                 library_id: str, access_token: str):
        self._name = name
        self._unique_id = unique_id
        self._library_id = library_id
        self._access_token = access_token
        self._state = "unknown"
        self._attributes = {}

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        headers = {
            "Authorization": f"Bearer {self._access_token}"
        }
        base_url = "https://api.spotify.com/v1"

        # 1. Prüfe Playlist
        playlist_url = f"{base_url}/playlists/{self._library_id}"
        resp = requests.get(playlist_url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            self._state = "playlist"
            self._attributes = {
                "name": data.get("name"),
                "id": data.get("id"),
                "type": "playlist",
                "images": data.get("images"),
            }
            return

        # 2. Prüfe Album
        album_url = f"{base_url}/albums/{self._library_id}"
        resp = requests.get(album_url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            self._state = "album"
            self._attributes = {
                "name": data.get("name"),
                "id": data.get("id"),
                "type": "album",
                "images": data.get("images"),
            }
            return

        # 3. Fallback
        self._state = "unknown"
        self._attributes = {}
