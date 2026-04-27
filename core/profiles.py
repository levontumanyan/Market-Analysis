from typing import Dict

from core.database.repository import DatabaseRepository


def get_profile_weights(
	repo: DatabaseRepository, profile_name: str = "balanced"
) -> Dict[str, float]:
	"""Return weight mapping for a given profile from the database"""
	weights = repo.get_profile_weights(profile_name.lower())

	if not weights:
		print(f"[Warning] Profile '{profile_name}' not found in DB. Using balanced.")
		weights = repo.get_profile_weights("balanced")
		if not weights:
			print(
				"[bold red]Error: 'balanced' profile also not found in DB. Cannot determine weights.[/bold red]"
			)
			return {}

	return weights
