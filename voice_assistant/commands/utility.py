from __future__ import annotations

from datetime import datetime


def get_time() -> str:
	now = datetime.now()
	return now.strftime("The time is %I:%M %p")


def get_date() -> str:
	today = datetime.today()
	return today.strftime("Today is %A, %B %d, %Y")


def greet() -> str:
	hour = datetime.now().hour
	if hour < 12:
		return "Good morning! How can I help you today?"
	if hour < 18:
		return "Good afternoon! What can I do for you?"
	return "Good evening! How may I assist you?"


def unknown_command() -> str:
	return "I'm not sure how to do that yet. Try 'help' for options."

