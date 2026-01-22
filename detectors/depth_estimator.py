import cv2
import torch
import numpy as np
import config
from depth_anything_v2.dpt import DepthAnythingV2

class DepthEstimator:
    def __init__(self):
        print(f"Loading DepthAnything V2 model: {config.DEPTH_MODEL_NAME} on {config.DEVICE}...")
        
        # Model config for VITS (Small) - consistent with config
        model_configs = {
            'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
            'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
            'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
            'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
        }
        
        # Default to vits (small) if not specified or inferred from filename
        encoder = 'vits' 
        if 'vitb' in config.DEPTH_MODEL_NAME: encoder = 'vitb'
        if 'vitl' in config.DEPTH_MODEL_NAME: encoder = 'vitl'
        
        self.model = DepthAnythingV2(**model_configs[encoder])
        
        # Load weights
        # Check if file exists, else might need download (handled manually by user for now as per plan/readme)
        try:
            self.model.load_state_dict(torch.load(config.DEPTH_MODEL_NAME, map_location='cpu'))
        except FileNotFoundError:
            print(f"WARNING: Depth model weights not found at {config.DEPTH_MODEL_NAME}. MDE will fail.")
            
        self.model = self.model.to(config.DEVICE).eval()

    def get_depth_map(self, frame):
        """
        Returns metric depth map (numpy array).
        """
        # infer_image returns depth
        depth = self.model.infer_image(frame) 
        return depth

    def get_person_depth(self, depth_map, bbox):
        """
        Calculate median depth for a person's bounding box.
        bbox: [x1, y1, x2, y2]
        """
        x1, y1, x2, y2 = map(int, bbox)
        # Clip to image bounds
        h, w = depth_map.shape
        x1 = max(0, x1); y1 = max(0, y1)
        x2 = min(w, x2); y2 = min(h, y2)
        
        if x1 >= x2 or y1 >= y2:
            return 0.0
            
        person_depth_roi = depth_map[y1:y2, x1:x2]
        return np.median(person_depth_roi)
