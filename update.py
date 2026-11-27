
#!/usr/bin/env python3

"""
HTML Find & Replace Patcher

Files required:
1. html_patcher.py
2. patches.txt

Features:
- Reads patches from a separate TXT file.
- Automatically applies FIND and REPLACE.
- Checks all patches before editing.
- Every FIND text must occur exactly once.
- Creates a timestamped HTML backup.
- If validation fails, nothing is changed.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


def main():
    print("\n=== HTML PATCHER ===\n")

    patch_file = Path(__file__).parent / "patches.txt"

    if not patch_file.is_file():
        print("ERROR: patches.txt not found!")
        input("\nPress Enter to exit...")
        return

    try:
        patches = json.loads(
            patch_file.read_text(encoding="utf-8")
        )
    except Exception as error:
        print("Invalid patches.txt format:", error)
        input("\nPress Enter to exit...")
        return

    if not isinstance(patches, list) or not patches:
        print("No patches found in patches.txt.")
        input("\nPress Enter to exit...")
        return

    html_input = "index.html"

    if not html_input:
        print("No HTML file entered.")
        input("\nPress Enter to exit...")
        return

    html_path = Path(html_input).expanduser()

    if not html_path.is_file():
        print("HTML file not found:", html_path)
        input("\nPress Enter to exit...")
        return

    try:
        original = html_path.read_text(encoding="utf-8")
    except Exception as error:
        print("Could not read HTML:", error)
        input("\nPress Enter to exit...")
        return

    updated = original
    errors = []

    # Validate every patch first
    for index, patch in enumerate(patches, 1):

        name = patch.get("name", f"Patch {index}")
        find_text = patch.get("find")
        replace_text = patch.get("replace")

        if not isinstance(find_text, str) or not find_text:
            errors.append(f"{name}: Invalid FIND text.")
            continue

        if not isinstance(replace_text, str):
            errors.append(f"{name}: Invalid REPLACE text.")
            continue

        count = updated.count(find_text)

        if count != 1:
            errors.append(
                f"{name}: Expected 1 match, found {count}."
            )
            continue

        updated = updated.replace(find_text, replace_text, 1)

    # Stop if any patch fails
    if errors:
        print("\nPATCH VALIDATION FAILED:\n")

        for error in errors:
            print(" -", error)

        print("\nHTML was NOT modified.")
        input("\nPress Enter to exit...")
        return

    if updated == original:
        print("No changes were necessary.")
        input("\nPress Enter to exit...")
        return

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = html_path.with_name(
        f"{html_path.stem}_backup_{timestamp}{html_path.suffix}"
    )

    try:
        shutil.copy2(html_path, backup_path)

        html_path.write_text(
            updated,
            encoding="utf-8"
        )

    except OSError as error:
        print("Could not update HTML:", error)
        print("Check the backup before retrying.")
        input("\nPress Enter to exit...")
        return

    print("\nSUCCESS!")
    print("Patches applied:", len(patches))
    print("Updated HTML:", html_path)
    print("Backup created:", backup_path)

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
