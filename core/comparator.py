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

    def _format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        if mins > 0:
            return f"{mins:02d}m {secs:02d}s"
        return f"{secs}s"

    def _print_header(self, text):
        print(f"\n\033[1m\033[36m{text}\033[0m")
        print(f"\033[36m{'-' * 60}\033[0m")

    def _print_kv(self, key, value):
        print(f"  \033[1m{key:<24}\033[0m {value}")

    def print_report(self):
        fps = self.processing_stats.get('fps', 30.0)
        total_frames = self.processing_stats.get('total_frames', 0)
        duration_sec = self.processing_stats.get('duration_sec', 0)
        video_duration = total_frames / fps if fps else 0

        # 1. Execution Summary
        self._print_header("EXECUTION REPORT")
        self._print_kv("Processing Time", f"{duration_sec:.2f}s ({self.processing_stats.get('fps', 0):.1f} fps)")
        self._print_kv("Video Duration", f"{self._format_time(video_duration)} ({total_frames} frames)")

        for method, data in self.stats.items():
            cost_reduction = 0.0
            if data['overlap_frames'] > 0:
                cost_reduction = (1 - (data['triggers'] / data['overlap_frames'])) * 100

            # 2. Method Metrics
            self._print_header(f"METHOD: {method.upper()}")
            self._print_kv("Overlapping Frames", f"{data['overlap_frames']}")
            self._print_kv("Interaction Frames", f"{data['interactions']}")

            # Triggers with color
            trigger_color = "\033[32m" if data['triggers'] < 10 else "\033[33m"
            self._print_kv("VLM Triggers", f"{trigger_color}{data['triggers']}\033[0m")

            # Savings with color
            savings_color = "\033[32m" if cost_reduction > 80 else ("\033[33m" if cost_reduction > 50 else "\033[31m")
            self._print_kv("VLM Cost Reduction", f"{savings_color}{cost_reduction:.1f}%\033[0m")

            # 3. Detailed Interaction Log
            if data['annotations']:
                print(f"\n  \033[1mDETECTED INTERACTIONS\033[0m")
                for i, ann in enumerate(data['annotations'], 1):
                    start_t = ann['start_frame'] / fps
                    end_t = ann['end_frame'] / fps
                    duration = end_t - start_t

                    is_triggered = ann.get('triggered', False)
                    status_icon = "🔥" if is_triggered else "✋"
                    status_text = "Triggered" if is_triggered else "Buffered"

                    time_range = f"[{self._format_time(start_t)} - {self._format_time(end_t)}]"

                    print(f"  {i}. {status_icon} {time_range} ({duration:.1f}s) - {status_text}")

        print(f"\033[36m{'-' * 60}\033[0m\n")
