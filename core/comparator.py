class Comparator:
    def __init__(self):
        self.stats = {
            'Heuristic': {'interactions': 0, 'triggers': 0, 'overlap_frames': 0},
            'MDE': {'interactions': 0, 'triggers': 0, 'overlap_frames': 0},
            'processed_frames': 0
        }

    def update(self, method_name, has_overlap, is_interaction, triggered):
        self.stats[method_name]['overlap_frames'] += 1 if has_overlap else 0
        self.stats[method_name]['interactions'] += 1 if is_interaction else 0
        self.stats[method_name]['triggers'] += 1 if triggered else 0

    def print_report(self):
        print("\n--- Comparator Report ---")
        for method, data in self.stats.items():
            if method == 'processed_frames': continue
            print(f"Method: {method}")
            print(f"  Overlaps detected: {data['overlap_frames']}")
            print(f"  Verified Interactions: {data['interactions']}")
            print(f"  VLM Triggers: {data['triggers']}")
            if data['overlap_frames'] > 0:
                reduction = (1 - (data['triggers'] / data['overlap_frames'])) * 100
                print(f"  VLM Cost Reduction: {reduction:.2f}%")
            print("-------------------------")
