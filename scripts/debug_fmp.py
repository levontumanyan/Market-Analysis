import os

import requests
from dotenv import load_dotenv

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"


def test_endpoint(name, url):
	print(f"Testing {name}...")
	# Try both Query Param and Header just to be sure
	params = {"apikey": FMP_API_KEY}

	try:
		response = requests.get(url, params=params)
		print(
			f"  URL: {response.url.replace(FMP_API_KEY, 'HIDDEN') if FMP_API_KEY else 'NO_KEY'}"
		)
		print(f"  Status: {response.status_code}")

		if response.status_code == 200:
			data = response.json()
			if data:
				print(f"  Success: Received {len(str(data))} bytes")
			else:
				print(
					"  Warning: Received empty list/dict (might be an invalid ticker or plan restriction)"
				)
		elif response.status_code == 403:
			print(
				"  Error 403: Forbidden. Your key is recognized but NOT authorized for this endpoint/tier."
			)
		elif response.status_code == 401:
			print(
				"  Error 401: Unauthorized. Your API key is likely invalid or missing."
			)
		else:
			print(f"  Error {response.status_code}: {response.text}")
	except Exception as e:
		print(f"  Exception: {e}")
	print("-" * 30)


def main():
	if not FMP_API_KEY:
		print("FAIL: FMP_API_KEY not found in .env file.")
		return

	ticker = "AAPL"

	# Test endpoints across different subscription tiers
	tests = [
		("Quote (Free/Basic)", f"{BASE_URL}/quote/{ticker}"),
		("Profile (Free/Basic)", f"{BASE_URL}/profile/{ticker}"),
		(
			"Key Metrics (Starter+)",
			f"{BASE_URL}/key-metrics/{ticker}?period=annual&limit=1",
		),
		("Ratios (Premium+)", f"{BASE_URL}/ratios/{ticker}?period=annual&limit=1"),
	]

	print(f"Starting FMP Troubleshooting for ticker: {ticker}\n")
	for name, url in tests:
		test_endpoint(name, url)


if __name__ == "__main__":
	main()
