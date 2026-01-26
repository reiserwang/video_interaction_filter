import cv2
import numpy as np
import networkx as nx
from collections import defaultdict
from scipy.spatial import distance
import config
from utils.geometry import bboxes_overlap

class InteractionFilter:
    def __init__(self, method='hybrid', pose_detector=None, depth_estimator=None):
        self.method = method # 'ipd', 'head', 'hybrid', 'mde'
        self.pose_detector = pose_detector
        self.depth_estimator = depth_estimator
        
        # Tracking state
        self.active_interactions = {} # pair -> {'count': int, 'start_frame': int, 'triggered': bool}
        self.frame_count = 0
        
    def _get_head_size(self, p, method='hybrid'):
        """
        Compute head size metric from keypoints.
        """
        kp = p['keypoints']
        conf = p['conf'] # This is average conf, but we need per-point conf. 
        # Recover per-point conf from the [x, y, c] structure in pose_detector
        
        left_eye_idx, right_eye_idx = 1, 2
        nose_idx = 0
        left_ear_idx, right_ear_idx = 3, 4
        head_indices = [nose_idx, left_eye_idx, right_eye_idx, left_ear_idx, right_ear_idx]
        
        # Check conf id based on kp shape
        # kp[i] = [x, y, conf]
        
        if method in ['ipd', 'hybrid']:
            if kp[left_eye_idx][2] > config.CONF_THRESHOLD and kp[right_eye_idx][2] > config.CONF_THRESHOLD:
                ipd = distance.euclidean(kp[left_eye_idx][:2], kp[right_eye_idx][:2])
                if ipd > 0: return ipd
        
        if method == 'ipd': return 0
        
        # Fallback to head width
        valid_points = [kp[i][0] for i in head_indices if kp[i][2] > config.CONF_THRESHOLD]
        if len(valid_points) < 2: return 0
        return max(valid_points) - min(valid_points)

    def _check_z_plane(self, v1, v2):
        if v1 == 0 or v2 == 0: return False

        if self.method == 'mde':
            # Metric or relative check?
            # If standard metric depth: abs(d1 - d2) / max(d1, d2)
            # DepthAnything outputs relative depth (inverse depth usually) for VITS unless calibrated.
            # Assuming relative depth: similar values = similar plane.
            diff_ratio = abs(v1 - v2) / max(abs(v1), abs(v2) + 1e-6)
            return diff_ratio < config.Z_PLANE_DEPTH_DIFF_THRESHOLD
        
        else:
            # Heuristic
            ratio = max(v1/v2, v2/v1)
            return ratio < config.Z_PLANE_RATIO_THRESHOLD

    def process(self, frame):
        self.frame_count += 1
        persons = self.pose_detector.detect(frame)
        
        ids = list(persons.keys())
        overlapping_pairs = set()
        interacting_pairs = set()
        
        # Pre-calc depth map if needed and if we have people
        depth_map = None
        if self.method == 'mde' and len(ids) > 1:
            depth_map = self.depth_estimator.get_depth_map(frame)

        # Pre-calculate z-metrics (O(N))
        z_metrics = {}
        if len(ids) > 1:
            for pid in ids:
                if self.method == 'mde':
                    if depth_map is not None:
                        z_metrics[pid] = self.depth_estimator.get_person_depth(depth_map, persons[pid]['bbox'])
                    else:
                        z_metrics[pid] = 0
                else:
                    z_metrics[pid] = self._get_head_size(persons[pid], self.method)

        # Graph for grouping
        G = nx.Graph()
        G.add_nodes_from(ids)
        
        # Standard O(N^2) check
        for i in range(len(ids)):
            id1 = ids[i]
            for j in range(i+1, len(ids)):
                id2 = ids[j]
                
                if bboxes_overlap(persons[id1]['bbox'], persons[id2]['bbox']):
                    pair = frozenset([id1, id2])
                    overlapping_pairs.add(pair)
                    
                    if self._check_z_plane(z_metrics[id1], z_metrics[id2]):
                        interacting_pairs.add(pair)
                        G.add_edge(id1, id2)

        # Identify groups
        groups = [list(c) for c in nx.connected_components(G) if len(c) > 1]

        # Update persistent interaction tracking
        threshold_frames = int(config.INTERACTION_DURATION_SEC / (config.FRAME_INTERVAL * 0.033)) # Approximate if FPS unknown, usually passed from main
        # We'll rely on Main to pass FPS or Config to set specific frames. 
        # Let's use config.INTERACTION_DURATION_SEC assuming 30fps for now or let logic handle it.
        # Actually proper way: count frames. 2 sec @ 30fps = 60 frames.
        
        frame_triggers = 0
        
        # Logic update
        current_pairs = interacting_pairs
        to_remove = []
        ended_interactions = []
        
        for pair, data in list(self.active_interactions.items()):
            if pair in current_pairs:
                data['count'] += 1
                # Trigger logic
                # 60 frames approx for 2s
                if data['count'] >= 60 and not data['triggered']:
                    frame_triggers += 1
                    data['triggered'] = True
                    data['trigger_frame'] = self.frame_count
            else:
                to_remove.append(pair)
        
        for r in to_remove:
            data = self.active_interactions[r]
            data['end_frame'] = self.frame_count - 1
            ended_interactions.append(data)
            del self.active_interactions[r]
            
        for pair in current_pairs:
            if pair not in self.active_interactions:
                self.active_interactions[pair] = { 'count': 1, 'start_frame': self.frame_count, 'triggered': False }
                
        return {
            'persons': persons,
            'interactions': interacting_pairs,
            'overlaps': overlapping_pairs,
            'groups': groups,
            'triggers': frame_triggers,
            'ended_interactions': ended_interactions,
            'active_interactions': self.active_interactions,
            'z_metrics': z_metrics
        }
