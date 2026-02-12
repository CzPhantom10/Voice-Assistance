from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from openai import OpenAI

from voice_assistant.config import load_settings
from voice_assistant.core.command_router import CommandRouter
from voice_assistant.core.recognizer import RecognizerConfig, SpeechRecognizer
from voice_assistant.core.speaker import Speaker, SpeakerConfig
from voice_assistant.ui.cli import CLI
from voice_assistant.utils.helpers import is_exit_command
from voice_assistant.utils.logger import get_logger


@dataclass
class AssistantConfig:
	wake_word: str
	language: str
	voice_mode_enabled: bool
	text_mode_enabled: bool
	logging_level: str
	stt_model: str
	llm_model: str


class VoiceAssistant:
	"""Main orchestrator for the CLI voice assistant."""

	def __init__(self, settings: Dict[str, Any]) -> None:
		self.settings = settings

		self.config = AssistantConfig(
			wake_word=settings["wake_word"],
			language=settings.get("language", "en-US"),
			voice_mode_enabled=settings.get("voice_mode_enabled", True),
			text_mode_enabled=settings.get("text_mode_enabled", True),
			logging_level=settings.get("logging", {}).get("level", "INFO"),
			stt_model=settings.get("stt", {}).get("model", "whisper-large-v3"),
			llm_model=settings.get("llm", {}).get("model", "llama-3.1-8b-instant"),
		)

		self.logger = get_logger(__name__, level=self.config.logging_level)
		self.cli = CLI()
		self.router = CommandRouter()

		stt_settings = settings.get("stt", {})
		self.recognizer = SpeechRecognizer(
			logger=self.logger,
			config=RecognizerConfig(
				wake_word=self.config.wake_word,
				language=self.config.language,
				use_groq=stt_settings.get("provider", "groq").lower() == "groq",
				groq_model=self.config.stt_model,
			),
		)

		tts_settings = settings.get("tts", {})
		self.speaker = Speaker(
			logger=self.logger,
			config=SpeakerConfig(
				enabled=tts_settings.get("enabled", True),
				provider=tts_settings.get("provider", "local"),
				rate=int(tts_settings.get("rate", 180)),
				volume=float(tts_settings.get("volume", 1.0)),
				voice=tts_settings.get("voice"),
			),
		)

		groq_settings = settings.get("groq", {})
		api_key = groq_settings.get("api_key")
		self.llm_client = None
		if api_key:
			self.llm_client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
		else:
			self.logger.warning("GROQ_API_KEY not configured; LLM Q&A will be basic.")

	def run(self) -> None:
		self.cli.render_banner()
		self.cli.show_message("assistant", "Type 'exit' or 'quit' at any time to stop.")

		mode = self.cli.prompt_mode(
			voice_enabled=self.config.voice_mode_enabled,
			text_enabled=self.config.text_mode_enabled,
		)

		if mode == "voice":
			self._run_voice_loop()
		else:
			self._run_text_loop()

	def _run_voice_loop(self) -> None:
		self.cli.show_status(f"Voice mode: say '{self.config.wake_word}' to wake me up.")

		while True:
			self.cli.show_status("Listening for wake word...")
			wake_text = self.recognizer.listen_once()
			if not wake_text:
				self.cli.show_error("I didn't catch that. Let's try again.")
				continue

			self.cli.show_message("user", wake_text)
			if is_exit_command(wake_text):
				self.cli.show_message("assistant", "Goodbye!")
				break

			if not self.recognizer.is_wake_word(wake_text):
				self.cli.show_status("That wasn't the wake word. Say it again or say 'exit' to quit.")
				continue

			self.cli.show_status("Wake word detected. Listening for your command...")
			command_text = self.recognizer.listen_once()
			if not command_text:
				self.cli.show_error("I couldn't hear your command.")
				continue

			self.cli.show_message("user", command_text)
			if is_exit_command(command_text):
				self.cli.show_message("assistant", "Goodbye!")
				break

			self._handle_command(command_text)

	def _run_text_loop(self) -> None:
		self.cli.show_status("Text mode: type your commands. Type 'exit' to quit.")
		while True:
			text = self.cli.prompt_text_command()
			if not text:
				continue
			if is_exit_command(text):
				self.cli.show_message("assistant", "Goodbye!")
				break
			self._handle_command(text)

	def _handle_command(self, text: str) -> None:
		route = self.router.route(text)

		if route.is_exit:
			self.cli.show_message("assistant", "Goodbye!")
			return

		if route.handler is None:
			if route.suggestions:
				suggestions_str = ", ".join(route.suggestions)
				self.cli.show_message(
					"assistant",
					f"I didn't recognize that command. Did you mean: {suggestions_str}? I'll also try to answer it as a question.",
				)
			response = self._answer_with_llm(text)
		else:
			try:
				response = route.handler(*route.args, **route.kwargs)
			except Exception as exc:
				self.logger.exception("Command handler failed: %s", exc)
				response = "Something went wrong while executing your command."

		self.cli.show_message("assistant", response)
		self.speaker.speak(response)

	def _answer_with_llm(self, prompt: str) -> str:
		if not self.llm_client:
			return "This is a placeholder response. Configure GROQ_API_KEY to enable rich answers."

		try:
			response = self.llm_client.responses.create(
				model=self.config.llm_model,
				input=[
					{
						"role": "system",
						"content": "You are a concise, helpful voice assistant.",
					},
					{"role": "user", "content": prompt},
				],
			)
			text = getattr(response, "output_text", None)
			if not text and hasattr(response, "output"):
				text = str(response.output)
			return text.strip() if text else "I couldn't generate a response right now."
		except Exception as exc:
			self.logger.error("Groq LLM call failed: %s", exc)
			return "I had trouble reaching the AI service. Please try again later."


def create_assistant() -> VoiceAssistant:
	settings = load_settings()
	return VoiceAssistant(settings=settings)

