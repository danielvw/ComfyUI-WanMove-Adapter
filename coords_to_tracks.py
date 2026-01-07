import torch
import torch.nn.functional as F
import numpy as np
import json

class CoordsToWanTracks:
    """ComfyUI Node: JSON Trajectories → WanMove TRACKS"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "coords": ("STRING", {"multiline": True, "default": ""}),
                "width": ("INT", {"default": 720}),
                "height": ("INT", {"default": 720}),
                "num_frames": ("INT", {"default": 81}),
                "normalized": ("BOOLEAN", {"default": False})  # True=0-1, False=pixel
            }
        }

    RETURN_TYPES = ("TRACKS",)
    FUNCTION = "convert"
    CATEGORY = "WanMove/Adapters"

    def convert(self, coords, width, height, num_frames, normalized):
        data = json.loads(coords)

        all_points = []
        for track in data:
            pts = []
            for p in track:
                pts.append([p["x"]/width, p["y"]/height])
            all_points.append(pts)

        pts_np = np.array(all_points, dtype=np.float32)  # shape (N, T_old, 2)
        pts_torch = torch.from_numpy(pts_np)
        pts_torch = pts_torch.permute(1,0,2)  # (T_old, N, 2)

        # --- Interpolation to desired frame count ---
        T_old, N, _ = pts_torch.shape
        if T_old != num_frames:
            pts_torch = F.interpolate(
                pts_torch.permute(1,2,0), size=num_frames, mode='linear', align_corners=True
            ).permute(2,0,1)

        # --- Pixel or normalized ---
        if not normalized:
            pts_torch[:,:,0] *= width
            pts_torch[:,:,1] *= height

        # --- Visibility ---
        visibility = torch.ones((num_frames, N), dtype=torch.bool)

        tracks = {
            "track_path": pts_torch,
            "track_visibility": visibility
        }

        return (tracks,)
