## 2024-05-22 - [CLI Progress Feedback]
**Learning:** CLI tools processing large files (like video) often feel "frozen" without immediate visual feedback. Users may terminate the process prematurely if they don't see progress within a few seconds.
**Action:** Always implement a progress bar (even a simple text-based one) for tasks taking > 2 seconds. Include FPS/ETA if possible to give users a sense of completion time.
