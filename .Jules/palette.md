## 2024-10-24 - CLI Progress Feedback
**Learning:** Users processing long videos need granular feedback (percentage/ETA) rather than just "still working" logs. In-place updates (`\r`) reduce console spam compared to newline logging.
**Action:** Use ANSI-based progress bars for long-running CLI tasks.
