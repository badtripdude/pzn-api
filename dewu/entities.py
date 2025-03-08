import abc
import json
from abc import ABC
from typing import Optional, List, Dict

NON_STATED = None
# class Product:
#     id: int
#     title: str
#     desc: str
#     images: list
#     category: str


class JsonSerializable(ABC):
    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_data):
        ...


class PoizonProductRaw(JsonSerializable):
    """
        получение сырых данных с пойзона (практически сырой json)

    """


    def __init__(self, price, detail, frontLabelSummaryDTO, lastSold, image, spuGroupList, saleProperties, basicParam,
                 favoriteData, brandRootInfo, sizeDto, relateProductInfo, shareInfo, skus):
        self.price: Dict = price
        self.detail: Dict = detail
        self.frontLabelSummaryDTO: Dict = frontLabelSummaryDTO
        self.lastSold: Optional[Dict] = lastSold
        self.image: Dict = image
        self.spuGroupList: Optional[Dict] = spuGroupList
        self.saleProperties: Optional[Dict] = saleProperties
        self.basicParam: Dict = basicParam
        self.favoriteData: Dict = favoriteData
        self.brandRootInfo: Optional[Dict] = brandRootInfo
        self.sizeDto: Optional[Dict] = sizeDto
        self.relateProductInfo: Optional[Dict] = relateProductInfo
        self.shareInfo: Optional[Dict] = shareInfo
        self.skus: Optional[List[Dict]] = skus

    @classmethod
    def from_json(cls, json_data):
        return cls(
            price=json_data.get('price'),
            detail=json_data.get('detail'),
            frontLabelSummaryDTO=json_data.get('frontLabelSummaryDTO'),
            lastSold=json_data.get('lastSold'),
            image=json_data.get('image'),
            spuGroupList=json_data.get('spuGroupList'),
            saleProperties=json_data.get('saleProperties'),
            basicParam=json_data.get('basicParam'),
            favoriteData=json_data.get('favoriteData'),
            brandRootInfo=json_data.get('brandRootInfo'),
            sizeDto=json_data.get('sizeDto'),
            relateProductInfo=json_data.get('relateProductInfo'),
            shareInfo=json_data.get('shareInfo'),
            skus=json_data.get('skus')
        )


class PoizonProduct(JsonSerializable):
    '''
    класс для хранения уже распарсенных данных
    '''
    def __init__(self,
                 product_params: Dict[str, str] | NON_STATED,
                 article: str,
                 category: str | NON_STATED,
                 category_id: int,
                 current_sizes: List[int] | NON_STATED,
                 current_colors: List[str] | NON_STATED,
                 size_ids: List[int] | NON_STATED,
                 color_ids: List[int] | NON_STATED,
                 prices: List[int] | NON_STATED,
                 sku_ids: List[int] | NON_STATED,
                 spu_id: int,
                 floor_price: int | NON_STATED,
                 current_images: List[str],
                 brand: str,
                 brand_logo: str,
                 brand_id: str,
                 title: str,
                 desc: str | NON_STATED,
                 size_table: Dict[str, str] | NON_STATED):
        self.product_params = product_params
        self.article = article
        self.category= category
        self.category_id = category_id
        self.current_sizes = current_sizes
        self.current_colors = current_colors
        self.size_ids = size_ids
        self.color_ids = color_ids
        self.prices = prices
        self.sku_ids = sku_ids  # уникальный
        self.spu_id = spu_id  # общий
        self.floor_price = floor_price
        self.current_images = current_images
        self.brand = brand
        self.brand_logo = brand_logo
        self.brand_id = brand_id
        self.title = title
        self.desc = desc
        self.size_table = size_table

    # картинки соотносятся по цветам не по размерам
    @classmethod
    def from_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)
        sku_ids, current_colors, current_sizes, prices, size_ids, color_ids, current_images = ([] for _ in range(7))
        size_table = {}
        # TODO товары с доставкой через европу убрать из списка
        for i in raw_data.skus:
            current_images.append(i['logoUrl'])
            sku_ids.append(i['skuId'])
            if 'price' in i:
                prices.append(i["price"]["prices"][0]["price"] if i["price"]["prices"] else NON_STATED)
            for j in i["properties"]:
                if 'saleProperty' in j:
                    if j["saleProperty"]["name"] == "颜色":
                        current_colors.append(j["saleProperty"]["value"])
                        color_ids.append(j["saleProperty"]["propertyValueId"])
                    elif j["saleProperty"]["name"] == "尺码":
                        current_sizes.append(j["saleProperty"]["value"])
                        size_ids.append(j["saleProperty"]["propertyValueId"])
        if "sizeInfo" in raw_data.sizeDto:
            for i in raw_data.sizeDto["sizeInfo"]["sizeTemplate"]["list"]:
                size_table[f"{i["sizeKey"]}"] = i["sizeValue"]
        product_params = {}
        for i in raw_data.basicParam['basicList']:
            product_params[i["key"]] = i["value"]

        if not product_params: product_params = NON_STATED
        if not current_sizes: current_sizes = NON_STATED
        if not current_colors: current_colors = NON_STATED
        if not size_ids: size_ids = NON_STATED
        if not color_ids: color_ids = NON_STATED
        if not prices: prices = NON_STATED
        if not sku_ids: sku_ids = NON_STATED
        if not size_table: size_table = NON_STATED

        return cls(
            product_params=product_params,
            article=raw_data.detail['articleNumber'],
            category=raw_data.detail.get("categoryName", NON_STATED),
            category_id=raw_data.detail["categoryId"],
            current_sizes=current_sizes,
            current_colors=current_colors,
            size_ids=size_ids,
            color_ids=color_ids,
            prices=prices,
            sku_ids=sku_ids,
            spu_id=raw_data.detail["spuId"],
            floor_price=raw_data.price["item"]["floorPrice"] if raw_data.price else None,
            current_images=current_images, brand=raw_data.brandRootInfo["brandItemList"][0]["brandName"],
            brand_logo=raw_data.brandRootInfo["brandItemList"][0]["brandLogo"],
            brand_id = raw_data.detail["brandId"],
            title=raw_data.detail["title"], desc=raw_data.detail["desc"] if raw_data.detail["desc"] else NON_STATED,
            size_table=size_table
        )

class PoizonCategoryParser(JsonSerializable):
    """
    класс для получения категорий api: GET /getCategories
    """
    def __init__(self, categories: Dict[str, str]):
        self.categories = categories

    @classmethod
    def from_json(cls, json_data):
        categories = {}
        for i in json_data:
            categories[i["id"]] = i["name"]
        return cls(categories = categories)


if (__name__ == "__main__"):
    with open('../jacket.json', 'r') as f:
        dictData = json.load(f)

    a = PoizonProduct.from_json(json_data=dictData)
    print(f"sizeIDs = {a.size_ids}")
    print(f"colorIds = {a.color_ids}")
    print(f"skuIds = {a.sku_ids}")
    print(f"current_sizes = {a.current_sizes}")
    print(f"current_colors = {a.current_colors}")
    print(f"prices = {a.prices}\n")
    print(f"brand = {a.brand}")
    print(f"brand_logo = {a.brand_logo}")

    print(f"brand_id = {a.brand_id}")
    print(f"spu_id = {a.spu_id}")
    print(f"floor_price = {a.floor_price}")
    print(f"title = {a.title}")
    print(f"desc = {a.desc}")
    print(f"current_images = {a.current_images}")
    print(f"category = {a.category}")
    print(f"category_id = {a.category_id}")
    print(f"size_table = {a.size_table}")
    print(f"product_params = {a.product_params}")
    print(f"article = {a.article}")
