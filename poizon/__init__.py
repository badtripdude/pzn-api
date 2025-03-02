import asyncio
import time
from typing import Unpack

import aiohttp
from aiohttp.client import _RequestOptions
from aiohttp.typedefs import StrOrURL

import entities


class Limiter:
    def __init__(self, requests_per_second):
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    def is_ok(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request >= self.min_interval:
            self.last_request_time = current_time
            return True
        else:
            return False

    def time_until_reset(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        return max(0.0, self.min_interval - time_since_last_request)


class ClientSession(aiohttp.ClientSession):
    def __init__(self, *args, **kwargs):
        self.limiter = Limiter(0.5)
        super().__init__(*args, **kwargs)

    async def request(
            self,
            method: str,
            url: StrOrURL,
            **kwargs: Unpack[_RequestOptions],
    ):
        if not self.limiter.is_ok():
            wait_time = self.limiter.time_until_reset()
            await asyncio.sleep(wait_time)
        return await super().request(method=method, url=url, **kwargs)


class Poizon:
    BASE_API = 'https://poizon-api.com/api/dewu/'

    def __init__(self, api_key):
        self.api_key = api_key
        self.session: aiohttp.ClientSession = None

    async def __aenter__(self):
        self.session = ClientSession(self.BASE_API, headers={
            'accept': 'application/json',
            'apikey': self.api_key
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_product_detail_with_price(self, spu_id: int):
        method = 'productDetailWithPrice'
        res = await self.session.request("GET", method, params={'spuId': spu_id})
        return entities.PoizonProduct.parse_json(await res.json())

    async def get_product_detail(self, spu_id: str):
        method = 'productDetail'
        res = await self.session.request("GET", method, params={'spuId': spu_id})
        return entities.PoizonProduct.parse_json(await res.json())

    async def search_products_v1(self, keyword: str, limit: int = 50, page: int = 0):
        method = 'searchProducts'
        response = await self.session.request("GET", method, params={'keyword': keyword,
                                                                     'limit': limit,
                                                                     'page': page})
        return await response.json()

    async def search_products_v2(self,
                                 keyword: str = None, lowest_price: int = None,
                                 highest_price: int = None, brand_id: list[int] = None,
                                 front_category_id: list[int] = None, category_id: list[int] = None,
                                 fit_id: list[int] = None, sort_type: int = None,
                                 sort_mode: int = None, limit: int = 50,
                                 page: int = 0,
                                 ):
        # TODO: params and enums
        method = 'searchProducts/v2'
        params = {
            'keyword': keyword,
            'lowestPrice': lowest_price,
            'highestPrice': highest_price,
            'limit': limit,
            'page': page,
        }  # TODO: add params
        filtered_params = {k: v for k, v in params.items() if v is not None}
        resp = await self.session.request('GET', method, params=filtered_params)

        return await resp.json()
