from os import environ
from elasticsearch import AsyncElasticsearch

from helpers.constants import ELASTIC_ASSET_INDEX, ELASTIC_EXCHANGE_INDEX


elasticsearch = AsyncElasticsearch(
	cloud_id=environ["ELASTICSEARCH_CLOUD_ID"],
	api_key=environ["ELASTICSEARCH_API_KEY"],
)


async def find_exchange(raw, platform):
	if platform in ["CoinGecko"]: return False, None

	query = {
		"bool": {
			"must": [{
				"multi_match": {"query": raw, "fields": ["id", "name", "triggers.name", "triggers.shortcuts"]}
			}, {
				"match": {"supports": platform}
			}]
		}
	}
	response = await elasticsearch.search(index=ELASTIC_EXCHANGE_INDEX, query=query, size=1)
	if response["hits"]["total"]["value"] > 0:
		exchange = response["hits"]["hits"][0]["_source"]
		return True, exchange
	return False, None