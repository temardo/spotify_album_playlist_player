# custom_components/spotify_album_playlist_player/helper.py
from homeassistant.core import HomeAssistant

class SpotifyHelper:
    @staticmethod
    def build_media_content_id(typ: str, lib_id: str) -> str:
        if typ == "playlist":
            return f"spotify:playlist:{lib_id}"
        elif typ == "album":
            return f"spotify:album:{lib_id}"
        return ""

    @staticmethod
    def play_library_item(hass: HomeAssistant, lib_id: str, typ: str):
        hass.services.call(
            "script",
            "spotify_playlist_abspielen",
            {
                "playlist_id": SpotifyHelper.build_media_content_id(typ, lib_id),
            },
        )
