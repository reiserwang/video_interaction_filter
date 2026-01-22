from ultralytics import YOLO
import numpy as np
import config

class PoseDetector:
    def __init__(self):
        print(f"Loading YOLO model: {config.YOLO_MODEL_NAME} on {config.DEVICE}...")
        self.model = YOLO(config.YOLO_MODEL_NAME)
        # Force device if possible (Ultralytics handles this internally usually, but good to be explicit if passed)
        # self.model.to(config.DEVICE) 

    def detect(self, frame):
        """
        Runs tracking on the frame.
        Returns:
            dict: { person_id: { 'bbox': [x1,y1,x2,y2], 'keypoints': [[x,y,conf], ...], 'conf': float } }
        """
        results = self.model.track(frame, persist=True, verbose=False, device=config.DEVICE)
        
        persons = {}
        if results[0].boxes is None or results[0].boxes.id is None:
            return persons

        ids = results[0].boxes.id.cpu().numpy().astype(int)
        bboxes = results[0].boxes.xyxy.cpu().numpy()
        
        # Keypoints: result is (N, 17, 2) usually xy, or (N, 17, 3) if conf included?
        # Ultralytics .keypoints.data is (N, 17, 3) [x, y, conf]
        # .keypoints.xy is (N, 17, 2)
        # .keypoints.conf is (N, 17)
        keypoints_xy = results[0].keypoints.xy.cpu().numpy()
        keypoints_conf = results[0].keypoints.conf.cpu().numpy()

        for i, person_id in enumerate(ids):
            # Combine xy and conf for easier processing later
            kps = []
            for j in range(len(keypoints_xy[i])):
                x, y = keypoints_xy[i][j]
                c = keypoints_conf[i][j] if keypoints_conf is not None else 0.0
                kps.append([x, y, c])

            persons[person_id] = {
                'bbox': bboxes[i],
                'keypoints': np.array(kps),
                'conf': np.mean(kps, axis=0)[2] # Average keypoint confidence as proxy
            }
        
        return persons
