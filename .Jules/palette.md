## 2024-05-23 - Robust CLI Feedback Patterns
**Learning:** CLI tools often neglect basic UX like progress bars and color. Using ANSI codes is a lightweight way to add delight without dependencies. Hardcoded keys in stats classes are a common source of crashes.
**Action:** Always check for dynamic keys in stats aggregators and wrap CLI output in a helper for consistent styling.

## 2024-10-24 - CLI Progress Pattern
**Learning:** CLI tools often lack visual feedback for long-running processes, causing user uncertainty.
**Action:** Use the lightweight `utils.cli.ProgressBar` for any frame-by-frame processing loop to provide immediate feedback on speed and ETA without adding heavy dependencies.

## 2025-02-27 - CLI Progress Bar Logging
**Learning:** Logging messages during a progress bar loop often breaks the visual layout, spamming the console and hiding the progress status.
**Action:** Implement a `log()` method on progress bars that clears the current line before printing, preserving the visual integrity of the progress indicator.
