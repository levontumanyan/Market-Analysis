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


# Global instance for tracking the current execution run
stats = SessionStats()
