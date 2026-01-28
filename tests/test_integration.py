import sys
import unittest
import numpy as np
from unittest.mock import MagicMock

# Mock dependencies before importing local modules
sys.modules['torch'] = MagicMock()
sys.modules['ultralytics'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['depth_anything_v2'] = MagicMock()
sys.modules['depth_anything_v2.dpt'] = MagicMock()

# Mock networkx specifically to handle logic
nx_mock = MagicMock()
sys.modules['networkx'] = nx_mock

sys.modules['scipy'] = MagicMock()
sys.modules['scipy.spatial'] = MagicMock()

import config
# import numpy as np # Already imported

# Mock config.DEVICE manually since config import might have failed or used mocked torch
config.DEVICE = 'cpu'
config.CONF_THRESHOLD = 0.5
config.INTERACTION_DURATION_SEC = 2.0
config.FRAME_INTERVAL = 1
config.Z_PLANE_DEPTH_DIFF_THRESHOLD = 0.1
config.Z_PLANE_RATIO_THRESHOLD = 1.3

from core.interaction_filter import InteractionFilter

class MockPoseDetector:
    def detect(self, frame):
        # Return synthetic persons
        # Scenario: Two people overlapping
        return {
            1: {'bbox': [100, 100, 200, 400], 'keypoints': np.ones((17, 3)), 'conf': 0.9},
            2: {'bbox': [150, 100, 250, 400], 'keypoints': np.ones((17, 3)), 'conf': 0.9}
        }

class MockDepthEstimator:
    def get_depth_map(self, frame):
        return np.ones((500, 500)) * 0.5 # Flat depth
        
    def get_person_depth(self, depth_map, bbox):
        return 0.5

class TestIntegration(unittest.TestCase):
    def test_interaction_trigger(self):
        # Setup specific mock behavior for networkx
        # We need connected_components to return a list of sets of IDs
        # Scenario: ID 1 and 2 are connected
        import networkx as nx # This gets the mock
        nx.connected_components.return_value = [{1, 2}]
        nx.Graph.return_value.add_nodes_from = MagicMock()
        nx.Graph.return_value.add_edge = MagicMock()

        # Configure scipy check
        # InteractionFilter imports 'distance' from scipy.spatial
        # We need to make sure distance.euclidean returns a number
        # Since we mocked sys.modules['scipy.spatial'], getting it from there:
        dist_mock = sys.modules['scipy.spatial'].distance
        dist_mock.euclidean.return_value = 10.0

        pose_mock = MockPoseDetector()
        depth_mock = MockDepthEstimator()
        
        # Test Heuristic
        f = InteractionFilter(method='hybrid', pose_detector=pose_mock)
        frame = np.zeros((500, 500, 3), dtype=np.uint8)
        
        # Run for enough frames to trigger (60 frames)
        triggered = False
        for _ in range(70):
            res = f.process(frame)
            if res['triggers'] > 0:
                triggered = True
                break
        
        self.assertTrue(triggered, "Hybrid method should trigger on overlap")
        
        # Test MDE
        f_mde = InteractionFilter(method='mde', pose_detector=pose_mock, depth_estimator=depth_mock)
        triggered_mde = False
        for _ in range(70):
            res = f_mde.process(frame)
            if res['triggers'] > 0:
                triggered_mde = True
                break
        
        self.assertTrue(triggered_mde, "MDE method should trigger on same depth")

if __name__ == '__main__':
    unittest.main()
