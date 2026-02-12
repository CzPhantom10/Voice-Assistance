from __future__ import annotations

import logging
from typing import Optional


_LOGGING_CONFIGURED = False


def _configure_root_logger(level: str = "INFO") -> None:
	global _LOGGING_CONFIGURED
	if _LOGGING_CONFIGURED:
		return

	numeric_level = getattr(logging, level.upper(), logging.INFO)
	logging.basicConfig(
		level=numeric_level,
		format="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
	)
	_LOGGING_CONFIGURED = True


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
	"""Return a configured logger instance.

	If ``level`` is provided, it is applied to the returned logger.
	"""

	if level:
		_configure_root_logger(level)
	else:
		_configure_root_logger()

	logger = logging.getLogger(name)
	if level:
		logger.setLevel(getattr(logging, level.upper(), logging.INFO))
	return logger

