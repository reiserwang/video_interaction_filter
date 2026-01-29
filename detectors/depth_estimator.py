import cv2
import torch
import torch.nn.functional as F
import numpy as np
import os
import config
from depth_anything_v2.dpt import DepthAnythingV2
from utils.cli import print_info

class DepthEstimator:
    def __init__(self):
        print_info(f"Loading DepthAnything V2 model: {config.DEPTH_MODEL_NAME} on {config.DEVICE}...")
        
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
        if os.path.exists(config.DEPTH_MODEL_NAME):
            print(f"\033[34mℹ\033[0m Loading DepthAnything V2 model: {config.DEPTH_MODEL_NAME} on {config.DEVICE}...") # Changed self.device to config.DEVICE
            # weights_only=False required for some older/complex weight files in newer PyTorch
            self.model.load_state_dict(torch.load(config.DEPTH_MODEL_NAME, map_location='cpu', weights_only=False))
            self.model.to(config.DEVICE).eval() # Changed self.device to config.DEVICE
        else:    print(f"WARNING: Depth model weights not found at {config.DEPTH_MODEL_NAME}. MDE will fail.")
            
        # The line below was redundant after the change, but was present in the instruction's snippet.
        # Keeping it as per instruction to faithfully reproduce the provided Code Edit,
        # but noting it might be a logical redundancy.
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
