from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class AssetType(Enum):
	STOCK = "STOCK"
	ETF = "ETF"
	INDEX = "INDEX"
	UNKNOWN = "UNKNOWN"


@dataclass
class AssetData:
	symbol: str
	asset_type: AssetType = AssetType.UNKNOWN
	name: Optional[str] = None
	sector: Optional[str] = None
	industry: Optional[str] = None
	metrics: Dict[str, Any] = field(default_factory=dict)
	raw_data: Dict[str, Any] = field(default_factory=dict)

	def get(self, key: str, default: Any = None) -> Any:
		"""
		Helper to get a metric or metadata field.
		Checks metrics first, then raw_data, then attributes.
		"""
		if key in self.metrics:
			return self.metrics[key]
		if key in self.raw_data:
			return self.raw_data[key]
		return getattr(self, key, default)

	@property
	def display_name(self) -> str:
		return self.name or self.symbol
