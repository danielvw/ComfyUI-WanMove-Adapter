from .coords_to_tracks import CoordsToWanTracks

NODE_CLASS_MAPPINGS = {
    "CoordsToWanTracks": CoordsToWanTracks
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CoordsToWanTracks": "Coords To WanMove Tracks"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
