from __future__ import annotations

from voice_assistant.core.assistant import create_assistant


def main() -> None:
	assistant = create_assistant()
	assistant.run()


if __name__ == "__main__":
	main()

