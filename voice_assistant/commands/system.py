from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path


def open_file_explorer(path: str | None = None) -> str:
	target = Path(path).expanduser().resolve() if path else Path.cwd()
	system = platform.system().lower()

	try:
		if system == "windows":
			os.startfile(str(target))
		elif system == "darwin":
			subprocess.Popen(["open", str(target)])
		else:
			subprocess.Popen(["xdg-open", str(target)])
		return f"Opening file explorer at {target}"
	except Exception:
		return "Sorry, I couldn't open the file explorer."


def system_info() -> str:
	return f"You are using {platform.system()} {platform.release()} on {platform.machine()} architecture."

