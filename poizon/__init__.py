import aiohttp


class Poizon:
    BASE_API = 'https://poizon-api.com/api/dewu/'

    def __init__(self, api_key):
        self.api_key = api_key
        self.session: aiohttp.ClientSession = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(self.BASE_API, headers={
            'accept': 'application/json',
            'apikey': self.api_key
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_product_detail_with_price(self, spu_id: int):
        method = 'productDetailWithPrice'
        res = await self.session.get(method, params={'spuId': spu_id})
        json = await res.json()
        print(json)

    async def get_product_detail(self, spu_id: str):
        method = 'productDetail'
        res = await self.session.get(method, params={'spuId': spu_id})
        json = await res.json()
        print(json)

    async def get_price_info