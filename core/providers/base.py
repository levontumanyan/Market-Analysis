from abc import ABC, abstractmethod
from typing import Optional

from core.schema import AssetData


class BaseProvider(ABC):
	@abstractmethod
	def get_data(self, symbol: str) -> Optional[AssetData]:
		"""Fetch and return normalized AssetData."""
		pass
