## Voice Assistant (CLI, Groq-powered)

A hackathon-grade, product-level voice assistant with a clean, modular architecture, a professional CLI interface, and modern AI integration via Groq.

This is not a toy script – it is structured as a v1.0 product you can confidently showcase in hackathons, demos, and on your resume.

---

## Features

- Wake word support ("OK Google") in voice mode
- Groq-based Speech-to-Text (with Google STT fallback)
- Pluggable Text-to-Speech (local TTS via `pyttsx3`, future Groq TTS hook)
- Command routing for:
	- System info and file explorer
	- Web search (Google)
	- YouTube search/open
	- Spotify song search (opens in browser)
- Text-mode CLI for debugging and non-mic environments
- Structured logging and centralized configuration

---

## Tech Stack

- **Language:** Python 3.10+
- **AI Backend:** Groq API (OpenAI-compatible)
- **Speech Recognition:** `SpeechRecognition` + Groq STT
- **Text-to-Speech:** `pyttsx3` (local), future-ready for Groq TTS
- **CLI UX:** Colorized output via `colorama`
- **Config & Env:** YAML (`PyYAML`), `.env` via `python-dotenv`

---

## Architecture Overview

The project follows a clean, modular architecture with clear separation of concerns:

- **Core:** Orchestration, STT/TTS, and command routing
- **Commands:** Concrete actions the assistant can perform
- **Config:** Settings and environment handling
- **Utils:** Logging and shared helpers
- **UI:** CLI-only, all user interaction is centralized here

High-level flow:

1. `main.py` bootstraps configuration and creates the `VoiceAssistant`.
2. The CLI shows a banner and prompts for interaction mode (voice/text).
3. In voice mode, the assistant listens for the wake word ("OK Google"), then records a command.
4. The command is routed to the appropriate handler (system, web, utility) or to the Groq LLM for Q&A.
5. The response is shown in the CLI and spoken via TTS (if enabled).

---

## Folder Structure

```text
voice_assistant/
	core/
		assistant.py          # Main control loop / orchestrator
		recognizer.py         # Speech-to-Text (Groq + fallback)
		speaker.py            # Text-to-Speech abstraction
		command_router.py     # Intent routing / command mapping

	commands/
		system.py             # OS/system-related commands
		web.py                # Browser, YouTube, Spotify search
		utility.py            # Time, date, greetings, unknown handling

	config/
		__init__.py           # Settings loader (.env + YAML)
		settings.yaml         # All configurable values

	utils/
		logger.py             # Structured logging helper
		helpers.py            # Text normalization, suggestions, safe access

	ui/
		cli.py                # Clean, colorized CLI UI

	main.py                 # Entry point for the CLI app

.env.example              # Example environment variables
requirements.txt          # Python dependencies
app1.py                   # Legacy Streamlit UI (deprecated)
```

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Voice-Assistance
```

2. **Create and activate a virtual environment (recommended)**

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

> Note: On Windows, installing `PyAudio` may require precompiled wheels.

4. **Configure environment variables**

Copy the example file and set your Groq API key:

```bash
copy .env.example .env
```

Then edit `.env` and set:

```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Review configuration**

All runtime configuration lives in:

- `voice_assistant/config/settings.yaml`

You can tweak:

- `wake_word`
- `language`
- `voice_mode_enabled` / `text_mode_enabled`
- Logging level
- STT/TTS providers and models
- Command toggles (Spotify, YouTube, web search, system)

---

## Running the Assistant

From the project root:

```bash
python -m voice_assistant.main
```

You will see a banner and be prompted to choose:

- **Voice mode** – microphone input + wake word ("OK Google")
- **Text mode** – type commands directly into the CLI

To exit at any time, say or type:

- `exit`, `quit`, or `stop`

---

## Environment Variables

The assistant reads sensitive values from environment variables (via `.env`).

Required:

- `GROQ_API_KEY` – your Groq API key for STT and LLM Q&A

Optional (can also be configured via YAML):

- `GROQ_STT_MODEL` – override STT model (e.g. `whisper-large-v3`)
- `GROQ_LLM_MODEL` – override LLM model (e.g. `llama-3.1-8b-instant`)

Never commit real keys; only commit `.env.example`.

---

## How It Works (Flow)

1. **Bootstrap**
	 - `.env` is loaded.
	 - `settings.yaml` is parsed.
	 - Logging is configured.

2. **Initialization**
	 - `SpeechRecognizer` is configured with wake word, language, and STT provider.
	 - `Speaker` is configured with TTS provider and voice options.
	 - `CommandRouter` prepares known commands and intent patterns.

3. **Interaction Loop**
	 - CLI asks for mode (voice/text).
	 - In **voice mode**:
		 - Listen for wake word.
		 - On wake word, capture a command.
	 - In **text mode**:
		 - Read commands from standard input.

4. **Routing & Execution**
	 - Command text is analyzed and routed to a handler (system/web/utility).
	 - If no handler matches, the text is sent to the Groq LLM for Q&A.
	 - The result is printed and (optionally) spoken.

---

## Sample Voice/Text Commands

- "OK Google" (wake word in voice mode)
- "What time is it?"
- "What's the date today?"
- "Open file explorer"
- "Search for Python decorators on Google"
- "Play lo-fi beats on Spotify"
- "Open YouTube for relaxing music"
- "What's the capital of France?" (handled by Groq LLM)

---

## Screenshots / Demo (Placeholders)

- `docs/screenshot-cli-banner.png` – CLI banner and mode selection
- `docs/screenshot-command-flow.png` – Example command and response

(You can add actual screenshots or a short GIF demo later.)

---

## Future Enhancements

The architecture is designed to support future extensions without major refactors:

- **GUI Version**
	- Tkinter or web-based UI sharing the same core assistant logic.

- **LLM-based Conversational Intelligence**
	- Multi-turn conversations with context memory.
	- Tool-using agents for web search, automation, etc.

- **Plugin System for Commands**
	- Discoverable plugins (e.g. `plugins/`) that auto-register commands.
	- Third-party integrations (calendar, email, smart home).

- **Multilingual Support**
	- Language selection in `settings.yaml`.
	- STT/TTS and LLM models configured per language.

- **Always-on Wake Word Engine**
	- Background service constantly listening for the wake word.
	- Hotword engine optimized for low CPU usage.

---

## Legacy Streamlit UI

The original Streamlit-based UI still exists as a legacy file:

- [app1.py](app1.py)

It has been intentionally deprecated in favor of the CLI-first architecture. All
new development should target the CLI (`voice_assistant/main.py`).

---

## License

Add your preferred license here (e.g. MIT) if you plan to open-source this project.
