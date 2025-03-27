import asyncio
import re
from typing import Unpack

import aiohttp
from aiohttp.client import _RequestOptions
from aiohttp.typedefs import StrOrURL

from . import enums
from .entities import JsonSerializable, PoizonProduct, ProductSearchResult
from .enums import SalesData
from .utils import Limiter


class ClientSession(aiohttp.ClientSession):
    REQUESTS_PER_SECOND = 0.5

    def __init__(self, *args, **kwargs):
        self.limiter = Limiter(self.REQUESTS_PER_SECOND)
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
        self._api_key = api_key
        self._session: aiohttp.ClientSession = None

    async def __aenter__(self):
        self._session = ClientSession(self.BASE_API, headers={
            'accept': 'application/json',
            'apikey': self._api_key
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def get_product_detail_with_price(self, spu_id: int) -> PoizonProduct:
        method = 'productDetailWithPrice'
        res = await self._session.request("GET", method, params={'spuId': spu_id})
        return entities.PoizonProduct.from_json(await res.json())

    async def get_product_detail(self, spu_id: str) -> PoizonProduct:
        method = 'productDetail'
        res = await self._session.request("GET", method, params={'spuId': spu_id})
        return entities.PoizonProduct.from_json(await res.json())

    async def search_products_v1(self, keyword: str, limit: int = 50, page: int = 0):
        method = 'searchProducts'
        response = await self._session.request("GET", method, params={'keyword': keyword,
                                                                      'limit': limit,
                                                                      'page': page})
        return await response.json()

    async def search_products_v2(self,
                                 keyword: str = None, lowest_price: int = None,
                                 highest_price: int = None, brand_id: list[int] = None,
                                 front_category_id: list[int] = None, category_id: list[int] = None,
                                 fit_id: list[enums.Gender] = None, sort_type: enums.SalesData = None,
                                 sort_mode: enums.SortMode = None, limit: int = 50,
                                 page: int = 0,
                                 ) -> ProductSearchResult:
        method = 'searchProducts/v2'
        params = {
            'keyword': keyword,
            'lowestPrice': lowest_price,
            'highestPrice': highest_price,
            'brandId': ','.join(map(str, brand_id)) if brand_id else None,
            'frontCategoryId': ','.join(map(str, front_category_id)) if front_category_id else None,
            'categoryId': ','.join(map(str, category_id)) if category_id else None,
            'fitId': ','.join(map(str, [f.value for f in fit_id])) if fit_id else None,
            'sortType': sort_type.value if sort_type else None,
            'sortMode': sort_mode.value if sort_mode else None,
            'limit': limit,
            'page': page,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}
        resp = await self._session.request('GET', method, params=filtered_params)

        return ProductSearchResult.from_json(await resp.json())

    async def extract_spu_id_by_url(self, url: str):
        url_pattern = re.compile(r'https?://[^\s]+')
        match = url_pattern.search(url)

        if not match:
            raise ValueError("URL не найден в переданной строке.")

        extracted_url = match.group(0)
        method = 'convertLinkToSpuId'
        response = await self._session.request("GET", method, params={'link': extracted_url})
        return await response.json()
