class Comparator:
    def __init__(self):
        self.stats = {}
        # Colors
        self.C_RESET = "\033[0m"
        self.C_BOLD = "\033[1m"
        self.C_GREEN = "\033[32m"
        self.C_BLUE = "\033[34m"
        self.C_RED = "\033[31m"
        self.C_CYAN = "\033[36m"

    def update(self, method_name, has_overlap, is_interaction, triggered):
        if method_name not in self.stats:
            self.stats[method_name] = {'interactions': 0, 'triggers': 0, 'overlap_frames': 0}

        self.stats[method_name]['overlap_frames'] += 1 if has_overlap else 0
        self.stats[method_name]['interactions'] += 1 if is_interaction else 0
        self.stats[method_name]['triggers'] += 1 if triggered else 0

    def print_report(self):
        print(f"\n{self.C_BOLD}{self.C_BLUE}--- Comparator Report ---{self.C_RESET}")
        if not self.stats:
            print("No data collected.")
            return

        for method, data in self.stats.items():
            print(f"{self.C_BOLD}Method: {self.C_CYAN}{method}{self.C_RESET}")
            print(f"  Overlaps detected: {data['overlap_frames']}")
            print(f"  Verified Interactions: {data['interactions']}")
            print(f"  VLM Triggers: {self.C_RED}{data['triggers']}{self.C_RESET}")
            if data['overlap_frames'] > 0:
                reduction = (1 - (data['triggers'] / data['overlap_frames'])) * 100
                print(f"  VLM Cost Reduction: {self.C_GREEN}{reduction:.2f}%{self.C_RESET}")
            else:
                # If there were no overlaps, we saved 100% of potential calls (assuming we would have called on overlap)
                # Or N/A. Let's say 100% efficient.
                print(f"  VLM Cost Reduction: {self.C_GREEN}N/A{self.C_RESET} (No overlaps)")
            print(f"{self.C_BLUE}-------------------------{self.C_RESET}")
