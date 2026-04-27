import time
from typing import Dict


class SessionStats:
	def __init__(self):
		self.cache_hits = 0
		self.api_calls = 0
		self.errors = 0
		self.stage_times: Dict[str, float] = {}
		self._stage_starts: Dict[str, float] = {}
		self.total_start_time = time.time()

	def start_stage(self, name: str):
		self._stage_starts[name] = time.time()

	def end_stage(self, name: str):
		if name in self._stage_starts:
			self.stage_times[name] = time.time() - self._stage_starts[name]

	def get_total_time(self) -> float:
		return time.time() - self.total_start_time

	def to_dict(self) -> Dict:
		"""Return the session statistics as a dictionary."""
		total_requests = self.cache_hits + self.api_calls
		cache_rate = (
			(self.cache_hits / total_requests * 100) if total_requests > 0 else 0
		)
		return {
			"total_duration_s": round(self.get_total_time(), 2),
			"cache_hits": self.cache_hits,
			"api_calls": self.api_calls,
			"cache_rate_pct": round(cache_rate, 2),
			"errors": self.errors,
			"stage_durations_s": {k: round(v, 2) for k, v in self.stage_times.items()},
		}


# Global instance for tracking the current execution run
stats = SessionStats()
