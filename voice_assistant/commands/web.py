from __future__ import annotations

import urllib.parse
import webbrowser


def open_web_search(query: str) -> str:
	encoded = urllib.parse.quote_plus(query)
	url = f"https://www.google.com/search?q={encoded}"
	webbrowser.open(url)
	return f"Searching the web for '{query}'."


def open_youtube_search(query: str) -> str:
	encoded = urllib.parse.quote_plus(query)
	url = f"https://www.youtube.com/results?search_query={encoded}"
	webbrowser.open(url)
	return f"Opening YouTube for '{query}'."


def open_spotify_search(song_query: str) -> str:
	encoded = urllib.parse.quote_plus(song_query)
	url = f"https://open.spotify.com/search/{encoded}"
	webbrowser.open(url)
	return f"Searching Spotify for '{song_query}'."

