## 2024-05-23 - Robust CLI Feedback Patterns
**Learning:** CLI tools often neglect basic UX like progress bars and color. Using ANSI codes is a lightweight way to add delight without dependencies. Hardcoded keys in stats classes are a common source of crashes.
**Action:** Always check for dynamic keys in stats aggregators and wrap CLI output in a helper for consistent styling.

## 2024-10-24 - CLI Progress Feedback
**Learning:** Users processing long videos need granular feedback (percentage/ETA) rather than just "still working" logs. In-place updates (`\r`) reduce console spam compared to newline logging.
**Action:** Use ANSI-based progress bars for long-running CLI tasks.
