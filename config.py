import torch
import os

# Device selection: MPS (Mac) > CUDA (NVIDIA) > CPU
if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

print(f"Using Device: {DEVICE}")

# Video processing
FRAME_INTERVAL = 1  # Process every Nth frame (1 = all frames)

# Interaction thresholds
INTERACTION_DURATION_SEC = 2.0  # Seconds of consistent overlap/z-plane to trigger
Z_PLANE_RATIO_THRESHOLD = 1.3  # Heuristic ratio
Z_PLANE_DEPTH_DIFF_THRESHOLD = 0.10  # 10% depth difference for MDE

# IPD/Head size constants
CONF_THRESHOLD = 0.5

# Model Weights
YOLO_MODEL_NAME = "yolov8n-pose.pt"
DEPTH_MODEL_NAME = "depth_anything_v2_vits.pth" # Metric Depth implementation might vary, using small visual transformer
