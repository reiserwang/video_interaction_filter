import cv2
from utils.geometry import get_bbox_center

def draw_detections(frame, persons, z_metrics=None):
    """
    Draw bounding boxes and keypoints for all detected persons.
    persons: dict of person_id -> {'bbox': ..., 'keypoints': ...}
    z_metrics: dict of person_id -> z_value (optional)
    """
    for person_id, data in persons.items():
        bbox = data['bbox']
        # Draw BBox
        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
        
        # Draw ID & Z-metric
        label = f"ID: {person_id}"
        if z_metrics and person_id in z_metrics:
            label += f" Z:{z_metrics[person_id]:.2f}"
            
        cv2.putText(frame, label, (int(bbox[0]), int(bbox[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Draw Keypoints (simplified)
        for kp in data['keypoints']:
            if kp[2] > 0.5: # confidence check if available, or just existence
                 cv2.circle(frame, (int(kp[0]), int(kp[1])), 3, (0, 255, 255), -1)

def draw_interactions(frame, interactions, persons):
    """
    Draw green lines for active interactions.
    interactions: list or set of (id1, id2) tuples
    """
    for id1, id2 in interactions:
        if id1 in persons and id2 in persons:
            pt1 = get_bbox_center(persons[id1]['bbox'])
            pt2 = get_bbox_center(persons[id2]['bbox'])
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

def draw_status(frame, frame_count, fps, method_name, vlm_triggers):
    """
    Overlay status text on the frame.
    """
    cv2.putText(frame, f"Frame: {frame_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"Method: {method_name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, f"VLM Triggers: {vlm_triggers}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
