import re

with open(r"C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\full_log.txt", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

output = []
for i, line in enumerate(lines):
    if "Fatal signal" in line or "DEBUG" in line and "crash" in line.lower() or "xash" in line.lower() or "cspb" in line.lower():
        # Get context (5 lines before, 10 lines after)
        start = max(0, i - 2)
        end = min(len(lines), i + 10)
        output.extend(lines[start:end])
        output.append("-" * 40 + "\n")

with open(r"C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\crash_summary.txt", "w", encoding="utf-8") as f:
    f.writelines(set(output)) # Use set to remove duplicates roughly
