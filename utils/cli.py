import sys
import time

class ProgressBar:
    """A simple text-based progress bar for CLI applications."""
    def __init__(self, total, width=40, prefix='Progress:', suffix='Complete'):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.suffix = suffix
        self.start_time = time.time()

    def update(self, current, extra_info=""):
        """Updates the progress bar in place."""
        if self.total <= 0:
            sys.stdout.write(f'\r{self.prefix} {current} processed {extra_info}')
            sys.stdout.flush()
            return

        percent = float(current) * 100 / self.total
        filled_length = int(self.width * current // self.total)
        bar = '█' * filled_length + '-' * (self.width - filled_length)

        elapsed_time = time.time() - self.start_time
        eta_str = ""
        if current > 0:
            eta = (elapsed_time / current) * (self.total - current)
            eta_str = f"ETA: {int(eta)}s"

        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent:.1f}% ({current}/{self.total}) {eta_str} {extra_info}')
        sys.stdout.flush()

    def finish(self):
        sys.stdout.write('\n')
        sys.stdout.flush()
