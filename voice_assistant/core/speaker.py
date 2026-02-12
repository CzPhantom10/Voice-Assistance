from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import pyttsx3


@dataclass
class SpeakerConfig:
	enabled: bool
	provider: str
	rate: int
	volume: float
	voice: Optional[str] = None


class Speaker:
	"""Text-to-speech abstraction."""

	def __init__(self, logger, config: SpeakerConfig) -> None:
		self.logger = logger
		self.config = config

		self._engine: Optional[pyttsx3.Engine] = None
		if self.config.enabled:
			self._setup_local_engine()

		if self.config.provider.lower() == "groq" and not os.getenv("GROQ_API_KEY"):
			self.logger.warning("Groq TTS selected but GROQ_API_KEY not set; using local TTS.")

	def _setup_local_engine(self) -> None:
		try:
			engine = pyttsx3.init()
			engine.setProperty("rate", self.config.rate)
			engine.setProperty("volume", self.config.volume)
			if self.config.voice:
				engine.setProperty("voice", self.config.voice)
			self._engine = engine
		except Exception as exc:
			self.logger.error("Failed to initialize local TTS engine: %s", exc)
			self._engine = None

	def speak(self, text: str) -> None:
		if not self.config.enabled:
			self.logger.info("TTS is disabled; skipping speech output.")
			return

		provider = self.config.provider.lower()
		if provider == "local" or self._engine is not None:
			self._speak_local(text)
		elif provider == "groq":
			self.logger.info("Groq TTS not implemented yet, falling back to local TTS.")
			self._speak_local(text)

	def _speak_local(self, text: str) -> None:
		if not self._engine:
			self.logger.warning("Local TTS engine not available; cannot speak.")
			return
		try:
			self._engine.say(text)
			self._engine.runAndWait()
		except Exception as exc:
			self.logger.error("Local TTS failed: %s", exc)

