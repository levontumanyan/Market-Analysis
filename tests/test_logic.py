from core.analysis.indices import get_index_components
from core.analysis.preprocessing import postprocess_score, preprocess_metric_value
from core.profiles import get_profile_weights
from core.schema import AssetData
from core.ui.formatters import format_display_value


def test_preprocess_metric_value():
	asset = AssetData(symbol="TEST", metrics={"dividendYield": 0.05})

	# Normal case
	assert preprocess_metric_value("dividendYield", 0.05, asset) == 0.05

	# Fallback case
	assert preprocess_metric_value("yield", None, asset) == 0.05

	# Institutional cap
	assert preprocess_metric_value("heldPercentInstitutions", 1.5, asset) == 1.0

	# Invalid data
	assert preprocess_metric_value("test", "not a number", asset) is None


def test_postprocess_score():
	# Negative P/E should result in 0 score
	assert postprocess_score("trailingPE", -5.0, 0.5) == 0.0
	# Normal case should be unchanged
	assert postprocess_score("trailingPE", 15.0, 0.5) == 0.5


def test_profile_weights_loading():
	weights = get_profile_weights("growth")
	assert isinstance(weights, dict)
	assert "revenueGrowth" in weights


def test_format_display_value():
	assert format_display_value(0.05, "percentage", True) == "5.00%"
	assert format_display_value(5.0, "percentage", False) == "5.00%"
	assert format_display_value(30.0, "multiplier") == "30.00x"
	assert format_display_value(100.5, "currency") == "$100.50"
	assert format_display_value(1.234, None) == "1.23"


def test_get_index_components(mocker):
	# Since it currently just returns the ticker, we test that behavior
	assert get_index_components("SPY") == ["SPY"]
