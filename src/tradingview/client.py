from aiohttp import ClientSession
from typing import Dict, List
from cachetools import TTLCache


class TradingViewSymbolSearchClient:
	def __init__(self, cache_ttl: int = 86400, cache_maxsize: int = 65536):
		self.base_url = "https://symbol-search.tradingview.com/symbol_search/v3/"
		self.cache = TTLCache(maxsize=cache_maxsize, ttl=cache_ttl)

		# Standard headers to mimic browser requests
		self.headers = {
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
			"Connection": "keep-alive",
			"Origin": "https://www.tradingview.com",
			"Referer": "https://www.tradingview.com/",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-site",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
		}

	async def search_symbols(
		self,
		query: str,
		exchange: str = "",
		search_type: str = "undefined",
		domain: str = "production",
		sort_by_country: str = "US",
		timeout: int = 10,
		use_cache: bool = True
	) -> List[Dict]:
		"""
		Search for symbols using the TradingView symbol search API.

		Args:
			query: The search query/symbol to look for
			exchange: Specific exchange to search in (optional)
			search_type: Type of search to perform (default: "undefined")
			domain: TradingView domain (default: "production")
			sort_by_country: Country to sort results by (default: "US")
			timeout: Request timeout in seconds (default: 10)
			use_cache: Whether to use caching (default: True)

		Returns:
			List of symbol dictionaries containing symbol information

		Raises:
			Exception: When API returns HTML response or other errors
			asyncio.TimeoutError: When request times out
		"""
		# Build the request URL
		params = {
			"text": query,
			"hl": 0,
			"exchange": exchange,
			"lang": "en",
			"search_type": search_type,
			"domain": domain,
			"sort_by_country": sort_by_country
		}

		# Create URL with parameters
		url = self.base_url + "?" + "&".join(f"{k}={v}" for k, v in params.items())
		print(url)

		# Check cache first if enabled
		if use_cache and url in self.cache:
			return self.cache[url]

		async with ClientSession() as session:
			async with session.get(url, headers=self.headers, timeout=timeout) as response:
				# Check if we got an HTML response (usually indicates an error)
				content_type = response.headers.get("Content-Type", "")
				if "text/html" in content_type:
					response_text = await response.text()
					raise Exception(f"TradingView API returned HTML response. Status: {response.status}, Response: {response_text}")

				# Parse JSON response
				response_data = await response.json()

				# Extract symbols from response
				symbols = response_data.get("symbols", [])

				# Cache the result if caching is enabled and query doesn't contain only digits
				if use_cache and not any(c.isdigit() for c in query):
					self.cache[url] = symbols

				return symbols[:10]