import sys
import time

class ProgressBar:
    """
    A simple progress bar for CLI applications.

    Usage:
        pb = ProgressBar(total=100)
        for i in range(100):
            pb.update(i + 1)
            time.sleep(0.1)
    """
    def __init__(self, total, prefix='', suffix='', decimals=1, length=50, fill='█', printEnd='\r'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd
        self.start_time = time.time()
        self.processed = 0

    def get_bar_string(self, iteration):
        """
        Generates the progress bar string for a given iteration.
        """
        if self.total == 0:
            percent = "100.0"
            filled_length = self.length
        else:
            percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))
            filled_length = int(self.length * iteration // self.total)

        bar = self.fill * filled_length + '-' * (self.length - filled_length)

        # Calculate FPS
        current_time = time.time()
        elapsed = current_time - self.start_time
        fps = iteration / elapsed if elapsed > 0 else 0.0

        return f'{self.prefix} |{bar}| {percent}% {self.suffix} [FPS: {fps:.1f}]'

    def update(self, iteration):
        """
        Updates the progress bar in the terminal.
        """
        self.processed = iteration
        bar_string = self.get_bar_string(iteration)
        sys.stdout.write(f'\r{bar_string}{self.printEnd}')
        sys.stdout.flush()

    def finish(self):
        """
        Clean up the progress bar.
        """
        sys.stdout.write('\n')
