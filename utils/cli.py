import sys
import time

class ProgressBar:
    """
    A simple, lightweight CLI progress bar.
    """
    def __init__(self, total=0, prefix='Progress', length=30, fill='█', color='\033[92m'):
        self.total = int(total) if total else 0
        self.prefix = prefix
        self.length = length
        self.fill = fill
        self.color = color
        self.reset = '\033[0m'
        self.start_time = time.time()
        self.last_update_time = 0

    def update(self, current, suffix=''):
        """
        Update the progress bar.
        current: current iteration (int)
        suffix: optional info to display (str)
        """
        # Throttle updates to ~10fps to avoid flickering and IO overhead
        now = time.time()
        if self.total > 0 and current < self.total and (now - self.last_update_time) < 0.1:
            return

        self.last_update_time = now

        elapsed_time = now - self.start_time
        speed = current / elapsed_time if elapsed_time > 0 else 0.0

        if self.total > 0:
            percent = min(100.0, 100 * (current / float(self.total)))
            filled_length = int(self.length * current // self.total)
            filled_length = min(self.length, filled_length) # Cap at length

            bar = self.fill * filled_length + '-' * (self.length - filled_length)

            remaining = self.total - current
            eta = remaining / speed if speed > 0 else 0
            eta_str = time.strftime("%H:%M:%S", time.gmtime(eta))

            # \r returns to start of line, end='' prevents newline
            # \033[K clears the line to avoid artifacts
            sys.stdout.write(f'\r\033[K{self.prefix} |{self.color}{bar}{self.reset}| {percent:.1f}% {suffix} [FPS: {speed:.1f} ETA: {eta_str}]')
        else:
            # Indeterminate state
            spinner = ['|', '/', '-', '\\'][current % 4]
            sys.stdout.write(f'\r\033[K{self.prefix} {spinner} {current} frames {suffix} [FPS: {speed:.1f}]')

        sys.stdout.flush()

    def log(self, message):
        """
        Log a message without corrupting the progress bar.
        Clears the current progress line, prints the message, and expects
        the next update() call to redraw the bar.
        """
        sys.stdout.write(f'\r\033[K{message}\n')
        sys.stdout.flush()

    def finish(self):
        """Clean up and print a newline."""
        sys.stdout.write('\n')
        sys.stdout.flush()
