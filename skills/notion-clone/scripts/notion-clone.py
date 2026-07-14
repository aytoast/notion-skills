import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path("notion")
PULL_SCRIPT = str(Path(__file__).resolve().parent.parent.parent / "notion-pull" / "scripts" / "notion-pull.py")

def main():
    if len(sys.argv) < 2:
        print("Usage: python notion-clone.py <id> [type: page|database]")
        return

    n_id = sys.argv[1]
    n_type = "page"
    if len(sys.argv) > 2:
        n_type = sys.argv[2]

    if not ROOT_DIR.exists():
        ROOT_DIR.mkdir()

    yaml_path = ROOT_DIR / "notion.yaml"
    yaml_path.write_text(f'type: "{n_type}"\nid: "{n_id}"\n', encoding="utf-8")

    print(f"Initialized clone tracking for {n_type} {n_id}")
    print("Running initial pull...")
    subprocess.run([sys.executable, PULL_SCRIPT])
    print("Clone complete.")

if __name__ == "__main__":
    main()
