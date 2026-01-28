import subprocess
import re
import sys
import time
import os

def run_benchmark(method, video_path="input.mp4", output_path=None):
    if output_path is None:
        output_path = f"output_{method}.mp4"
    
    cmd = [
        sys.executable, "main.py",
        "--video", video_path,
        "--method", method,
        "--output", output_path
    ]
    
    print(f"Running benchmark for method: {method}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {method}: {e}")
        print(e.stdout)
        print(e.stderr)
        return None

    end_time = time.time()
    total_time = end_time - start_time
    
    # Extract FPS and Total Frames from output if available, or calculate
    # Looking for "Processing: 100% | 308/308 [00:10<00:00, 28.56it/s]| Triggers: 0" style output
    # But main.py also prints a summary at the end via comparator.print_report()
    
    # We can also parse the "Done." or specific stats if main.py prints them.
    # Let's rely on the output from 'comparator.print_report()' which usually prints stats.
    # If not, we can calculate FPS simply as Total Frames / Total Time.
    
    frames_match = re.search(r'"total_frames":\s*(\d+)', output)
    fps_match = re.search(r'"fps":\s*([\d\.]+)', output)
    savings_match = re.search(r'"cost_reduction_percent":\s*([\d\.]+)', output)
    
    total_frames = int(frames_match.group(1)) if frames_match else 0
    fps = float(fps_match.group(1)) if fps_match else (total_frames / total_time if total_time > 0 else 0)
    savings = float(savings_match.group(1)) if savings_match else 0.0
    
    return {
        "method": method,
        "total_time": total_time,
        "fps": fps,
        "total_frames": total_frames,
        "savings": savings
    }

def main():
    video_path = "input.mp4"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        return

    methods = ["hybrid", "mde"]
    results = []

    print(f"Starting benchmark on {video_path}...\n")

    for method in methods:
        res = run_benchmark(method, video_path)
        if res:
            results.append(res)
        print("-" * 40)

    print("\nBenchmark Results:")
    print(f"{'Method':<10} | {'Time (s)':<10} | {'FPS':<10} | {'Frames':<10} | {'Savings (%)':<12}")
    print("-" * 65)
    
    for res in results:
        print(f"{res['method']:<10} | {res['total_time']:<10.2f} | {res['fps']:<10.2f} | {res['total_frames']:<10} | {res['savings']:<12.1f}")

if __name__ == "__main__":
    main()
