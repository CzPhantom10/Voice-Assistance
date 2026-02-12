from __future__ import annotations

import difflib
from typing import Iterable, List, Optional


def normalize_text(text: str) -> str:
	return " ".join(text.strip().lower().split())


def suggest_closest(text: str, candidates: Iterable[str], *, n: int = 3) -> List[str]:
	"""Return up to ``n`` closest matches from ``candidates`` for ``text``."""

	return difflib.get_close_matches(text, list(candidates), n=n, cutoff=0.5)


def is_exit_command(text: str) -> bool:
	normalized = normalize_text(text)
	return normalized in {"exit", "quit", "stop", "q"}


def safe_get(mapping: dict, *keys: str, default: Optional[object] = None):
	current = mapping
	for key in keys:
		if not isinstance(current, dict) or key not in current:
			return default
		current = current[key]
	return current

