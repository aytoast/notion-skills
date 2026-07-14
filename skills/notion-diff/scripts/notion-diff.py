import os
import sys
import json
import difflib
from pathlib import Path

ROOT_DIR = Path("notion")

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def print_diff(shadow_lines, local_lines):
    sm = difflib.SequenceMatcher(None, shadow_lines, local_lines)
    has_changes = False

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        has_changes = True

        if tag == "replace":
            for line in shadow_lines[i1:i2]:
                print(f"{Colors.RED}- {line}{Colors.RESET}")
            for line in local_lines[j1:j2]:
                print(f"{Colors.GREEN}+ {line}{Colors.RESET}")
        elif tag == "delete":
            for line in shadow_lines[i1:i2]:
                print(f"{Colors.RED}- {line}{Colors.RESET}")
        elif tag == "insert":
            for line in local_lines[j1:j2]:
                print(f"{Colors.GREEN}+ {line}{Colors.RESET}")

    return has_changes

def page_body(page_md_path):
    content = page_md_path.read_text(encoding="utf-8")
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            return content[end + 4:].lstrip("\r\n").rstrip()
    return content.rstrip()

def diff_page(page_md_path, page_shadow):
    local_content = page_body(page_md_path)
    if isinstance(page_shadow, dict):
        shadow_content = page_shadow.get("markdown", "")
    else:
        shadow_content = "\n\n".join(b.get("md_line", "") for b in page_shadow)
    local_content_lines = local_content.splitlines()
    shadow_lines = shadow_content.splitlines()

    if shadow_lines == local_content_lines:
        return False

    print(f"\nDiff for {page_md_path}:")
    return print_diff(shadow_lines, local_content_lines)

def main():
    if not ROOT_DIR.exists():
        print("No notion directory found. Run notion clone first.")
        return

    index_file = ROOT_DIR / ".notion-index.json"
    if not index_file.exists():
        print("No shadow index found. Run notion pull first.")
        return

    try:
        shadow_index = json.loads(index_file.read_text("utf-8"))
    except Exception as e:
        print(f"Error reading shadow index: {e}")
        return

    changes_found = False

    for root, dirs, files in os.walk(ROOT_DIR):
        root_path = Path(root)
        page_md = root_path / "page.md"
        if page_md.exists():
            yaml_path = root_path / "notion.yaml"
            if yaml_path.exists():
                lines = yaml_path.read_text("utf-8").splitlines()
                page_id = None
                for line in lines:
                    if "id:" in line:
                        page_id = line.split(":", 1)[1].strip().strip('"').strip("'")

                if page_id and page_id in shadow_index:
                    if diff_page(page_md, shadow_index[page_id]):
                        changes_found = True

    if not changes_found:
        print("Workspace is clean. No local changes detected.")

if __name__ == "__main__":
    main()
