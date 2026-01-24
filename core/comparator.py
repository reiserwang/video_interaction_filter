import json
from collections import defaultdict

class Comparator:
    def __init__(self):
        # Stats per method
        # Structure: { method_name: { 'interactions': 0, 'triggers': 0, 'overlap_frames': 0, 'annotations': [] } }
        self.stats = defaultdict(lambda: {
            'interactions': 0,
            'triggers': 0,
            'overlap_frames': 0,
            'annotations': []
        })
        self.processing_stats = {}

    def update(self, method_name, has_overlap, is_interaction, triggered):
        self.stats[method_name]['overlap_frames'] += 1 if has_overlap else 0
        self.stats[method_name]['interactions'] += 1 if is_interaction else 0
        self.stats[method_name]['triggers'] += 1 if triggered else 0

    def log_interaction(self, method_name, start_frame, end_frame, triggered, trigger_frame=None):
        self.stats[method_name]['annotations'].append({
            'start_frame': start_frame,
            'end_frame': end_frame,
            'triggered': triggered,
            'trigger_frame': trigger_frame
        })

    def set_processing_stats(self, start_time, end_time, duration, fps, total_frames):
        self.processing_stats = {
            'start_time': start_time,
            'end_time': end_time,
            'duration_sec': duration,
            'fps': fps,
            'total_frames': total_frames
        }

    def print_report(self):
        # Enrich annotations with timestamps if FPS is available
        fps = self.processing_stats.get('fps', 30.0) # Default to 30 if not set

        output = {
            'processing_stats': self.processing_stats,
            'methods': {}
        }

        for method, data in self.stats.items():
            # Calculate cost reduction
            cost_reduction = 0.0
            if data['overlap_frames'] > 0:
                cost_reduction = (1 - (data['triggers'] / data['overlap_frames'])) * 100

            # Enrich annotations
            enriched_annotations = []
            for ann in data['annotations']:
                start_time_sec = ann['start_frame'] / fps
                end_time_sec = ann['end_frame'] / fps

                # Format MM:SS
                ann_enriched = ann.copy()
                ann_enriched['start_time'] = f"{int(start_time_sec // 60):02d}:{int(start_time_sec % 60):02d}"
                ann_enriched['end_time'] = f"{int(end_time_sec // 60):02d}:{int(end_time_sec % 60):02d}"
                enriched_annotations.append(ann_enriched)

            output['methods'][method] = {
                'metrics': {
                    'overlaps': data['overlap_frames'],
                    'interactions': data['interactions'],
                    'triggers': data['triggers'],
                    'cost_reduction_percent': round(cost_reduction, 2)
                },
                'annotations': enriched_annotations
            }

        print(json.dumps(output, indent=2))
