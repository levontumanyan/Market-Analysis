import json

from core.yf_client import get_yf_data


def test_get_yf_data_cache_hit(mocker, tmp_path):
	# Setup cache dir
	cache_dir = tmp_path / "cache"
	cache_dir.mkdir()
	mocker.patch("core.yf_client.CACHE_DIR", cache_dir)

	ticker = "AAPL"
	cache_file = cache_dir / f"{ticker}.json"
	mock_data = {"symbol": "AAPL", "price": 150}
	cache_file.write_text(json.dumps(mock_data))

	# Ensure file is fresh
	# result = get_yf_data(ticker)
	# assert result["price"] == 150

	# We need to mock the stat().st_mtime to be recent
	mocker.patch("os.path.exists", return_value=True)
	# Actually, easier to just mock the time.time()
	mocker.patch("time.time", return_value=cache_file.stat().st_mtime + 100)

	result = get_yf_data(ticker)
	assert result["symbol"] == "AAPL"


def test_get_yf_data_fetch_logic(mocker, tmp_path):
	# Mock yfinance Ticker and cache dir
	cache_dir = tmp_path / "cache"
	cache_dir.mkdir()
	mocker.patch("core.yf_client.CACHE_DIR", cache_dir)

	mock_ticker = mocker.Mock()
	mock_ticker.info = {"symbol": "MSFT", "sharesOutstanding": 1000}
	mock_ticker.get_shares_full.return_value = None  # Simplify for now
	mocker.patch("yfinance.Ticker", return_value=mock_ticker)
	mocker.patch("time.sleep")  # Disable rate limit sleep

	result = get_yf_data("MSFT")
	assert result["symbol"] == "MSFT"
	assert (cache_dir / "MSFT.json").exists()
