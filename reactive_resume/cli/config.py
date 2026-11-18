"""CLI Configuration and Client Resolution."""

import json
import os
from pathlib import Path
from typing import Any

from reactive_resume import RxResumeClient

CONFIG_DIR = Path.home() / ".config" / "rxresume"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict[str, Any]:
    """Load config file if it exists, or return empty default structure."""
    if not CONFIG_FILE.is_file():
        return {"current_profile": "default", "profiles": {"default": {}}}
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"current_profile": "default", "profiles": {"default": {}}}


def save_config(config: dict[str, Any]) -> None:
    """Save config data to ~/.config/rxresume/config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_client(
    url: str | None = None,
    api_key: str | None = None,
    token: str | None = None,
    profile: str | None = None,
) -> RxResumeClient:
    """Resolve configuration precedence and return an initialized RxResumeClient."""
    config = load_config()
    profile_name = profile or config.get("current_profile", "default")
    profile_data = config.get("profiles", {}).get(profile_name, {})

    resolved_url = (
        url or os.environ.get("RX_RESUME_URL") or profile_data.get("url") or "https://rxresu.me"
    )
    resolved_api_key = api_key or os.environ.get("RX_RESUME_API_KEY") or profile_data.get("api_key")
    resolved_token = token or os.environ.get("RX_RESUME_TOKEN") or profile_data.get("token")

    return RxResumeClient(
        base_url=resolved_url,
        api_key=resolved_api_key,
        token=resolved_token,
    )
