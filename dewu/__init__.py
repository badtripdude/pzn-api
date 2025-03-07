import asyncio
import time
from typing import Unpack

import aiohttp
from aiohttp.client import _RequestOptions
from aiohttp.typedefs import StrOrURL

from .entities import JsonSerializable, PoizonProduct


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


class ProductSearchCard(JsonSerializable):
    def __init__(self, title: str = None, spu_id: int = None,
                 logo_url: str = None, images: list[str] = None, article_number: str = None,
                 price: int = None, min_sale_price: int = None, max_sale_price: int = None,
                 spu_min_sale_price: int = None, sku_id: int = None, level1_category_id: int = None,
                 category_id: int = None, brand_id: int = None, brand_name: str = None,
                 brand_logo_url: str = None):
        self.level1_category_id = level1_category_id
        self.max_sale_price = max_sale_price
        self.brand_name = brand_name
        self.min_sale_price = min_sale_price
        self.sku_id = sku_id
        self.spu_min_sale_price = spu_min_sale_price
        self.brand_id = brand_id
        self.brand_logo_url = brand_logo_url
        self.category_id = category_id
        self.price = price
        self.article_number = article_number
        self.images = images
        self.spu_id = spu_id
        self.logo_url = logo_url
        self.title = title

    @classmethod
    def from_json(cls, json_data):
        # TODO
        return cls(
            title=json_data.get('title'),
            spu_id=json_data.get('spuId'),
            logo_url=json_data.get('logoUrl'),
            images=json_data.get('images'),

        )


class ProductSearchResult(JsonSerializable):
    def __init__(self,
                 total: int, page: int, last_id: str = None,
                 product_list: list[ProductSearchCard] = None,
                 ):
        self.product_list = product_list
        self.last_id = last_id
        self.page = page
        self.total = total

    @classmethod
    def from_json(cls, json_data):
        return cls(
            total=json_data['total'],
            page=json_data['page'],
            last_id=json_data.get('lastId', None),
            product_list=[ProductSearchCard.from_json(data) for data in json_data.get('productList', [])]
        )


class Poizon:
    # TODO: handle http errors
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

    async def get_product_detail_with_price(self, spu_id: int) -> PoizonProduct:
        method = 'productDetailWithPrice'
        res = await self.session.request("GET", method, params={'spuId': spu_id})
        return entities.PoizonProduct.from_json(await res.json())

    async def get_product_detail(self, spu_id: str) -> PoizonProduct:
        method = 'productDetail'
        res = await self.session.request("GET", method, params={'spuId': spu_id})
        return entities.PoizonProduct.from_json(await res.json())

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
                                 ) -> ProductSearchResult:
        # TODO: enums
        method = 'searchProducts/v2'
        params = {
            'keyword': keyword,
            'lowestPrice': lowest_price,
            'highestPrice': highest_price,
            'brandId': brand_id,
            'frontCategoryId': front_category_id,
            'categoryId': category_id,
            'fitId': fit_id,
            'sortType': sort_type,
            'sortMode': sort_mode,
            'limit': limit,
            'page': page,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}
        resp = await self.session.request('GET', method, params=filtered_params)

        return ProductSearchResult.from_json(await resp.json())
