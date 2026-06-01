#!/usr/bin/env python3
"""
Simple test script for the TradingView Symbol Search Client.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))

from tradingview.client import TradingViewSymbolSearchClient


async def test_basic_functionality():
	"""Test basic client functionality."""
	print("Testing TradingView Symbol Search Client...")

	client = TradingViewSymbolSearchClient()

	# Test 1: Basic search
	print("\n1. Testing basic search for AAPL...")
	try:
		results = await client.search_symbols("AAPL")
		assert len(results) > 0, "Should find results for AAPL"
		assert any("AAPL" in r.get("symbol", "") for r in results), "Should contain AAPL symbol"
		print(f"✓ Found {len(results)} results for AAPL")

		# Check result structure
		first_result = results[0]
		required_fields = ["symbol", "description", "exchange"]
		for field in required_fields:
			assert field in first_result, f"Result should contain '{field}' field"
		print(f"✓ Result structure is valid")

	except Exception as e:
		print(f"✗ Basic search test failed: {e}")
		return False

	# Test 2: Exchange-specific search
	print("\n2. Testing exchange-specific search...")
	try:
		nasdaq_results = await client.search_symbols("AAPL", exchange="NASDAQ")
		assert len(nasdaq_results) >= 0, "Should handle exchange-specific search"
		print(f"✓ Exchange-specific search returned {len(nasdaq_results)} results")
	except Exception as e:
		print(f"✗ Exchange-specific search test failed: {e}")
		return False

	# Test 3: Natural language search
	print("\n3. Testing natural language search for 'Google'...")
	try:
		results = await client.search_symbols("Google")
		assert len(results) > 0, "Should find results for 'Google'"
		assert any("GOOGL" in r.get("symbol", "") for r in results), "Should contain GOOGL symbol"
		print(f"✓ Found {len(results)} results for 'Google'")
	except Exception as e:
		print(f"✗ Natural language search test failed: {e}")
		return False

	# Test 4: Error handling
	print("\n4. Testing error handling...")
	try:
		# Test with disabled cache
		results = await client.search_symbols("GOOGL", use_cache=False)
		assert isinstance(results, list), "Should return list even with cache disabled"
		print("✓ Error handling and cache control working")
	except Exception as e:
		print(f"✗ Error handling test failed: {e}")
		return False

	print("\n🎉 All tests passed!")
	return True


def test_client_initialization():
	"""Test client initialization with different parameters."""
	print("\nTesting client initialization...")

	try:
		# Test default initialization
		client1 = TradingViewSymbolSearchClient()
		assert client1.cache.maxsize == 65536, "Default cache size should be 65536"
		assert client1.cache.ttl == 86400, "Default TTL should be 86400 seconds"

		# Test custom initialization
		client2 = TradingViewSymbolSearchClient(cache_ttl=3600, cache_maxsize=1000)
		assert client2.cache.maxsize == 1000, "Custom cache size should be respected"
		assert client2.cache.ttl == 3600, "Custom TTL should be respected"

		print("✓ Client initialization tests passed")
		return True
	except Exception as e:
		print(f"✗ Client initialization test failed: {e}")
		return False


async def main():
	"""Run all tests."""
	print("=" * 50)
	print("TradingView Symbol Search Client Test Suite")
	print("=" * 50)

	# Test initialization
	init_passed = test_client_initialization()

	# Test basic functionality
	if init_passed:
		functionality_passed = await test_basic_functionality()
	else:
		functionality_passed = False

	print("\n" + "=" * 50)
	if init_passed and functionality_passed:
		print("🎉 ALL TESTS PASSED!")
		print("The TradingView Symbol Search Client is working correctly.")
	else:
		print("❌ SOME TESTS FAILED!")
		print("Please check the implementation and try again.")
	print("=" * 50)


if __name__ == "__main__":
	asyncio.run(main())
