import argparse
import cv2
import sys
import time
from datetime import datetime
import config
from core.interaction_filter import InteractionFilter
from core.comparator import Comparator
from detectors.pose_detector import PoseDetector
from detectors.depth_estimator import DepthEstimator
from utils.visualization import draw_detections, draw_interactions, draw_status
from utils.cli import ProgressBar

def main():
    parser = argparse.ArgumentParser(description="Smart Video Interaction Filter")
    parser.add_argument("--video", type=str, required=True, help="Input video path")
    parser.add_argument("--output", type=str, default="output.mp4", help="Output video path")
    parser.add_argument("--method", type=str, default="hybrid", choices=['ipd', 'head', 'hybrid', 'mde'], help="Z-plane detection method")
    parser.add_argument("--device", type=str, default=None, help="Device override")
    args = parser.parse_args()
    
    # Config override
    if args.device:
        config.DEVICE = args.device

    # Initialize Detectors
    pose_detector = PoseDetector()
    depth_estimator = None
    if args.method == 'mde':
        depth_estimator = DepthEstimator()

    # Initialize Filter
    interaction_filter = InteractionFilter(
        method=args.method, 
        pose_detector=pose_detector, 
        depth_estimator=depth_estimator
    )
    
    # Initialize Comparator
    comparator = Comparator()
    
    # Video Setup
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit(1)
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(args.output, fourcc, fps, (width, height))
    
    frame_count = 0
    total_triggers = 0
    
    print(f"Starting processing: {args.video} -> {args.output} using {args.method}")

    start_time_wall = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_time = time.time()
    results = {}

    progress = ProgressBar(total=total_frames, prefix='Processing')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Process
        results = interaction_filter.process(frame)
        
        # Stats update
        has_overlap = len(results['overlaps']) > 0
        has_interaction = len(results['interactions']) > 0
        triggers = results['triggers']
        total_triggers += triggers
        
        comparator.update(args.method, has_overlap, has_interaction, triggers > 0)
        
        # Log ended interactions
        for interaction in results.get('ended_interactions', []):
            comparator.log_interaction(
                args.method,
                interaction['start_frame'],
                interaction['end_frame'],
                interaction['triggered'],
                interaction.get('trigger_frame')
            )

        # Draw
        draw_detections(frame, results['persons'])
        draw_interactions(frame, results['interactions'], results['persons'])
        draw_status(frame, frame_count, fps, args.method, total_triggers)
        
        out.write(frame)
        
        progress.update(frame_count)

    progress.finish()
    cap.release()
    out.release()
    
    # Log remaining active interactions as ended
    for pair, data in results.get('active_interactions', {}).items():
        comparator.log_interaction(
            args.method,
            data['start_frame'],
            frame_count,
            data['triggered'],
            data.get('trigger_frame')
        )

    end_time = time.time()
    duration = end_time - start_time
    end_time_wall = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    comparator.set_processing_stats(start_time_wall, end_time_wall, duration, fps, frame_count)
    comparator.print_report()
    print("Done.")

if __name__ == "__main__":
    main()
