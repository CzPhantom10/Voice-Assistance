from __future__ import annotations

from typing import Literal

from colorama import Fore, Style, init as colorama_init


Mode = Literal["voice", "text"]


class CLI:
	"""Console-based UI for the voice assistant.

	All user-facing prints should go through this class.
	"""

	def __init__(self) -> None:
		colorama_init(autoreset=True)

	def render_banner(self) -> None:
		title = f"{Fore.CYAN}{Style.BRIGHT}Voice Assistant v1.0{Style.RESET_ALL}"
		border = f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}"
		print(border)
		print(title)
		print(f"{Fore.CYAN}Hackathon-ready CLI assistant powered by Groq AI{Style.RESET_ALL}")
		print(border)

	def show_message(self, sender: str, message: str) -> None:
		if sender.lower() == "assistant":
			prefix = f"{Fore.GREEN}[Assistant]{Style.RESET_ALL}"
		elif sender.lower() == "user":
			prefix = f"{Fore.BLUE}[You]{Style.RESET_ALL}"
		else:
			prefix = f"{Fore.MAGENTA}[{sender}]{Style.RESET_ALL}"
		print(f"{prefix} {message}")

	def show_status(self, message: str) -> None:
		print(f"{Fore.YELLOW}[Status]{Style.RESET_ALL} {message}")

	def show_error(self, message: str) -> None:
		print(f"{Fore.RED}[Error]{Style.RESET_ALL} {message}")

	def prompt_mode(self, *, voice_enabled: bool, text_enabled: bool) -> Mode:
		options = []
		if voice_enabled:
			options.append("1. Voice mode (microphone + wake word)")
		if text_enabled:
			options.append("2. Text mode (type commands)")

		self.show_status("Select interaction mode:")
		for line in options:
			print(f"  {line}")

		while True:
			choice = input("Enter choice [1/2]: ").strip()
			if choice == "1" and voice_enabled:
				return "voice"
			if choice == "2" and text_enabled:
				return "text"
			self.show_error("Invalid choice. Please enter 1 or 2.")

	def prompt_text_command(self) -> str:
		return input(f"{Fore.BLUE}You > {Style.RESET_ALL}").strip()

