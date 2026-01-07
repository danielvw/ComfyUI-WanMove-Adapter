import sys
import json
import torch
import matplotlib.pyplot as plt

sys.path.append("./custom_nodes/ComfyUI-WanMove-Adapter")
from coords_to_tracks import CoordsToWanTracks

# Example JSON
coords_json = json.dumps([
    [
        {"x": 355, "y": 148},
        {"x": 355, "y": 150},
        {"x": 358, "y": 156},
        {"x": 363, "y": 165},
        {"x": 369, "y": 174},
        {"x": 377, "y": 183},
        {"x": 387, "y": 189},
        {"x": 400, "y": 192},
        {"x": 415, "y": 192},
        {"x": 435, "y": 191}
    ]
])

width = 720
height = 720
num_frames = 81

node = CoordsToWanTracks()
tracks_tuple = node.convert(coords=coords_json, width=width, height=height, num_frames=num_frames, normalized=False)
tracks = tracks_tuple[0]

print("track_path shape:", tracks["track_path"].shape)
print("track_visibility shape:", tracks["track_visibility"].shape)
print("track_path min/max:", tracks["track_path"].min().item(), tracks["track_path"].max().item())
print("track_visibility unique values:", torch.unique(tracks["track_visibility"]))

# Plot
path = tracks["track_path"][:,0,:].numpy()
plt.plot(path[:,0], path[:,1], marker='o')
plt.gca().invert_yaxis()
plt.title("Test Trajektorie")
plt.show()
