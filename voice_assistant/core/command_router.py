from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple

from voice_assistant.commands import system, utility, web
from voice_assistant.utils.helpers import normalize_text, suggest_closest


Handler = Callable[..., str]


@dataclass
class RouteResult:
	handler: Optional[Handler]
	args: Tuple[Any, ...]
	kwargs: Dict[str, Any]
	suggestions: Tuple[str, ...] = ()
	is_exit: bool = False


class CommandRouter:
	"""Map natural language text to concrete command handlers."""

	def __init__(self) -> None:
		self._registry: Dict[str, Handler] = {
			"time": lambda: utility.get_time(),
			"date": lambda: utility.get_date(),
			"greet": lambda: utility.greet(),
			"system_info": lambda: system.system_info(),
			"open_explorer": lambda: system.open_file_explorer(),
			"search_web": lambda q: open_web_search_wrapper(q),
			"search_youtube": lambda q: web.open_youtube_search(q),
			"search_spotify": lambda q: web.open_spotify_search(q),
		}

	@property
	def known_commands(self) -> Tuple[str, ...]:
		return tuple(self._registry.keys())

	def route(self, text: str) -> RouteResult:
		original = text
		text = normalize_text(text)

		if text in {"exit", "quit", "stop", "q"}:
			return RouteResult(handler=None, args=(), kwargs={}, is_exit=True)

		if "time" in text:
			return RouteResult(handler=self._registry["time"], args=(), kwargs={})
		if "date" in text or "day" in text:
			return RouteResult(handler=self._registry["date"], args=(), kwargs={})
		if any(word in text for word in ["hello", "hi", "hey", "greet"]):
			return RouteResult(handler=self._registry["greet"], args=(), kwargs={})

		if "spotify" in text or "song" in text or "music" in text:
			query = (
				original.lower()
				.replace("play", "")
				.replace("on spotify", "")
				.replace("spotify", "")
			).strip()
			return RouteResult(handler=self._registry["search_spotify"], args=(query or original,), kwargs={})

		if "youtube" in text:
			query = (
				original.lower()
				.replace("play", "")
				.replace("on youtube", "")
				.replace("youtube", "")
			).strip()
			return RouteResult(handler=self._registry["search_youtube"], args=(query or original,), kwargs={})

		if any(word in text for word in ["search", "google", "look up"]):
			query = original.lower().replace("search", "").replace("google", "").strip()
			return RouteResult(handler=self._registry["search_web"], args=(query or original,), kwargs={})

		suggestions = suggest_closest(text, self.known_commands)
		return RouteResult(handler=None, args=(), kwargs={}, suggestions=tuple(suggestions))


def open_web_search_wrapper(query: str) -> str:
	from voice_assistant.commands import web as web_cmds

	return web_cmds.open_web_search(query)

