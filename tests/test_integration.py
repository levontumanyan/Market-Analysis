from core.data import get_stock_data, load_benchmarks
from core.orchestrator import run_bulk_analysis
from core.profiles import get_profile_weights


def test_load_benchmarks_invalid_file():
	# Test with a non-existent file
	assert load_benchmarks("non_existent.json") == []


def test_run_bulk_analysis(mocker):
	# Mock analyze_asset to avoid hitting the network/provider
	mock_res = {"symbol": "AAPL", "score": 80.0}
	mocker.patch("core.orchestrator.analyze_asset", return_value=mock_res)

	callback_called = False

	def callback(res):
		nonlocal callback_called
		callback_called = True

	results = run_bulk_analysis(["AAPL"], "balanced", progress_callback=callback)

	assert len(results) == 1
	assert results[0]["symbol"] == "AAPL"
	assert callback_called


def test_get_profile_weights_invalid():
	# Test fallback to balanced if profile not found
	weights = get_profile_weights("invalid_profile_name")
	assert isinstance(weights, dict)
	assert len(weights) > 0  # Should fallback to balanced which has weights


def test_get_stock_data(mocker):
	# Mock the provider to avoid real API calls
	mocker.patch("core.data.OpenBBProvider.get_data", return_value="mocked_data")
	assert get_stock_data("AAPL") == "mocked_data"
