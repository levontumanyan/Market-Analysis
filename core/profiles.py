import json
from typing import Any, Dict

from config import PROFILES_PATH


def load_profiles() -> Dict[str, Any]:
	"""Load all profiles from the configured profiles path"""
	try:
		with open(PROFILES_PATH, "r") as f:
			data = json.load(f)
		return data.get("profiles", {})
	except FileNotFoundError:
		print(f"[bold red]Error: {PROFILES_PATH} not found.[/bold red]")
		return {}
	except json.JSONDecodeError:
		print(
			f"[bold red]Error: Could not decode JSON from {PROFILES_PATH}.[/bold red]"
		)
		return {}


def get_profile_weights(profile_name: str = "balanced") -> Dict[str, float]:
	"""Return weight mapping for a given profile"""
	profiles = load_profiles()
	profile = profiles.get(profile_name.lower())

	if not profile:
		print(f"[Warning] Profile '{profile_name}' not found. Using balanced.")
		profile = profiles.get("balanced")
		if not profile:
			print(
				"[bold red]Error: 'balanced' profile also not found. Cannot determine weights.[/bold red]"
			)
			return {}

	return profile.get("weights", {})
