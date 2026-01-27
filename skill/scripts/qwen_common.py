import os
import re
from pathlib import Path


def _load_dotenv_file(p: Path) -> None:
    """Minimal .env loader (KEY=VALUE). Does not override existing env."""
    if not p.exists():
        return
    for raw in p.read_text("utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if not k:
            continue
        os.environ.setdefault(k, v)


def load_env() -> None:
    """Load env vars in Baoyu-style precedence.

    Priority (low -> high):
      1) ~/.baoyu-skills/.env
      2) <repo>/.baoyu-skills/.env (walk upwards from this file)
      3) existing process env always wins (we never override)

    This makes it easy to keep keys out of the repo while still supporting
    project-local setup.
    """
    # user-level
    _load_dotenv_file(Path.home() / ".baoyu-skills" / ".env")

    # project-level: walk up from this file and look for .baoyu-skills/.env
    cur = Path(__file__).resolve()
    for parent in [cur.parent, *cur.parents]:
        envp = parent / ".baoyu-skills" / ".env"
        if envp.exists():
            _load_dotenv_file(envp)
            break


def get_dashscope_key() -> str:
    """Get DASHSCOPE_API_KEY from env; fallback to ~/.bashrc export line."""
    load_env()

    key = os.getenv("DASHSCOPE_API_KEY")
    if key:
        return key.strip()

    bashrc = Path.home() / ".bashrc"
    if bashrc.exists():
        s = bashrc.read_text("utf-8", errors="ignore")
        m = re.search(r"export\s+DASHSCOPE_API_KEY=['\"]([^'\"]+)['\"]", s)
        if m:
            return m.group(1).strip()

    raise RuntimeError("DASHSCOPE_API_KEY not found in env, .baoyu-skills/.env, or ~/.bashrc")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)
