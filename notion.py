import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

SKILLS_DIR = ROOT_DIR / "skills"
CLONE_SCRIPT = str(SKILLS_DIR / "notion-clone" / "scripts" / "notion-clone.py")
PULL_SCRIPT = str(SKILLS_DIR / "notion-pull" / "scripts" / "notion-pull.py")
DIFF_SCRIPT = str(SKILLS_DIR / "notion-diff" / "scripts" / "notion-diff.py")
PUSH_SCRIPT = str(SKILLS_DIR / "notion-push" / "scripts" / "notion-push.py")

def main():
    if len(sys.argv) < 2:
        print("Usage: python notion.py <command> [args...]")
        print("Commands: clone, diff, pull, push")
        return

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "clone":
        subprocess.run([sys.executable, CLONE_SCRIPT, *args])
    elif cmd == "pull":
        subprocess.run([sys.executable, PULL_SCRIPT, *args])
    elif cmd == "diff":
        subprocess.run([sys.executable, DIFF_SCRIPT, *args])
    elif cmd == "push":
        subprocess.run([sys.executable, PUSH_SCRIPT, *args])
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: clone, diff, pull, push")

if __name__ == "__main__":
    main()
