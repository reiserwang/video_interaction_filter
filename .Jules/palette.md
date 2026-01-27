## 2024-05-23 - Robust CLI Feedback Patterns
**Learning:** CLI tools often neglect basic UX like progress bars and color. Using ANSI codes is a lightweight way to add delight without dependencies. Hardcoded keys in stats classes are a common source of crashes.
**Action:** Always check for dynamic keys in stats aggregators and wrap CLI output in a helper for consistent styling.

## 2024-10-24 - CLI Progress Pattern
**Learning:** CLI tools often lack visual feedback for long-running processes, causing user uncertainty.
**Action:** Use the lightweight `utils.cli.ProgressBar` for any frame-by-frame processing loop to provide immediate feedback on speed and ETA without adding heavy dependencies.

## 2024-01-27 - CLI Progress/Log Collision
**Learning:** Mixing standard `print` statements with `\r` based progress bars causes visual glitches and broken output.
**Action:** Implement a `log()` method on the progress bar class that clears the line, prints the message, and forces a redraw, ensuring clean logs without interrupting the progress visual.
