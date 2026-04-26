import time

import yfinance as yf


def test_bulk_capabilities():
	tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

	print("--- Testing yf.download() ---")
	# yf.download is primarily for OHLCV data
	try:
		download_data = yf.download(
			tickers, period="1d", group_by="ticker", progress=False
		)
		print(f"yf.download keys: {list(download_data.keys())}")
		print(
			"Conclusion: yf.download returns price data (Open, High, Low, Close, Volume)."
		)
	except Exception as e:
		print(f"yf.download error: {e}")

	print("\n--- Testing yf.Tickers() (plural) ---")
	# yf.Tickers returns an object with a .tickers dict
	try:
		group = yf.Tickers(" ".join(tickers))
		# Note: Accessing .info still triggers individual requests under the hood in many versions
		start = time.time()
		aapl_info = group.tickers["AAPL"].info
		print(f"Time to get one info from group: {time.time() - start:.2f}s")
		print(f"AAPL Sector: {aapl_info.get('sector')}")
	except Exception as e:
		print(f"yf.Tickers error: {e}")


if __name__ == "__main__":
	test_bulk_capabilities()
