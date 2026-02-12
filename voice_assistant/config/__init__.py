from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "settings.yaml"


def _load_dotenv() -> None:
	"""Load environment variables from a .env file at project root, if present."""

	env_path = PROJECT_ROOT / ".env"
	load_dotenv(dotenv_path=env_path if env_path.exists() else None)


@lru_cache(maxsize=1)
def load_settings(config_path: Path | None = None) -> Dict[str, Any]:
	"""Load YAML settings for the assistant.

	The result is cached for the lifetime of the process.
	"""

	_load_dotenv()

	path = config_path or DEFAULT_CONFIG_PATH
	if not path.exists():
		raise FileNotFoundError(f"Settings file not found: {path}")

	with path.open("r", encoding="utf-8") as f:
		settings: Dict[str, Any] = yaml.safe_load(f) or {}

	groq_api_key = os.getenv("GROQ_API_KEY")
	if groq_api_key:
		settings.setdefault("groq", {})["api_key"] = groq_api_key

	return settings

