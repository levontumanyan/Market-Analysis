from core.analysis.indices import get_index_components


def test_get_index_components_etf():
	# SPY is a well-known ETF, it should return top holdings
	components = get_index_components("SPY")
	assert len(components) > 1
	assert "AAPL" in components or "MSFT" in components or "NVDA" in components


def test_get_index_components_mutual_fund():
	# VFIAX is a mutual fund tracking S&P 500
	components = get_index_components("VFIAX")
	assert len(components) > 1
	assert "AAPL" in components or "MSFT" in components or "NVDA" in components


def test_get_index_components_fallback():
	# ^GSPC is an index, yfinance usually fails to give holdings via funds_data
	# It should return the ticker itself as fallback
	components = get_index_components("^GSPC")
	assert components == ["^GSPC"]


def test_get_index_components_invalid():
	# Invalid ticker should return itself
	components = get_index_components("INVALID_TICKER_123")
	assert components == ["INVALID_TICKER_123"]
