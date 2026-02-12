from __future__ import annotations

import io
import os
from dataclasses import dataclass
from typing import Any, Optional

import speech_recognition as sr
from openai import OpenAI

from voice_assistant.utils.helpers import normalize_text


@dataclass
class RecognizerConfig:
	wake_word: str
	language: str
	use_groq: bool
	groq_model: str


class SpeechRecognizer:
	"""Wrapper around microphone + Groq/OpenAI-compatible STT.

	Uses Groq's OpenAI-compatible audio transcription endpoint when
	``use_groq`` is True and ``GROQ_API_KEY`` is configured; otherwise
	falls back to the local Google Web Speech API via SpeechRecognition.
	"""

	def __init__(self, logger, config: RecognizerConfig) -> None:
		self.logger = logger
		self.config = config
		self._recognizer = sr.Recognizer()
		self._client: Optional[OpenAI] = None

		if self.config.use_groq:
			api_key = os.getenv("GROQ_API_KEY")
			if not api_key:
				self.logger.warning("GROQ_API_KEY not set; disabling Groq STT.")
				self.config.use_groq = False
			else:
				self._client = OpenAI(
					api_key=api_key,
					base_url="https://api.groq.com/openai/v1",
				)

	def listen_once(self, *, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> Optional[str]:
		"""Capture a single utterance from the default microphone and transcribe it."""

		try:
			with sr.Microphone() as source:
				self.logger.info("Adjusting for ambient noise...")
				self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
				self.logger.info("Listening for speech input...")
				audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
		except Exception as exc:
			self.logger.error("Microphone error: %s", exc)
			return None

		return self._transcribe_audio(audio)

	def _transcribe_audio(self, audio: sr.AudioData) -> Optional[str]:
		if self.config.use_groq and self._client is not None:
			try:
				wav_bytes = audio.get_wav_data()
				file_obj = io.BytesIO(wav_bytes)
				file_obj.name = "audio.wav"

				self.logger.info("Sending audio to Groq STT model '%s'", self.config.groq_model)
				response = self._client.audio.transcriptions.create(
					model=self.config.groq_model,
					file=file_obj,
				)
				text = getattr(response, "text", None) or getattr(response, "output_text", None)
				if not text:
					self.logger.error("Groq STT response did not contain text field.")
					return None
				return text.strip()
			except Exception as exc:
				self.logger.error("Groq STT failed, falling back to Google: %s", exc)

		try:
			text = self._recognizer.recognize_google(audio, language=self.config.language)
			return text.strip()
		except Exception as exc:
			self.logger.error("Speech recognition failed: %s", exc)
			return None

	def is_wake_word(self, text: str) -> bool:
		return normalize_text(text) == normalize_text(self.config.wake_word)

