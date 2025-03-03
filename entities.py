import json
from typing import Optional, List, Dict
from unicodedata import category


# class Product:
#     id: int
#     title: str
#     desc: str
#     images: list
#     category: str




# parsing from json into ProductContainer
#product Detail - floorPrice, spuID, skuID imgs, brand, brandLogo, detail.title, detail.desc
class PoizonProductRaw:
    def __init__(self, price, detail, frontLabelSummaryDTO, lastSold, image, spuGroupList, saleProperties, basicParam, favoriteData, brandRootInfo, sizeDto, relateProductInfo, shareInfo, skus):
        self.price: Dict= price
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


# product Detail
class PoizonProduct:
    def __init__(self, category, current_sizes, current_colors, sizeIds, colorIds, prices, skuIds, spuId, floor_price, all_images, brand, brand_logo, title, desc):
        self.category: str = category
        self.current_sizes: List[int] = current_sizes
        self.current_colors: List[str] = current_colors
        self.sizeIds: Optional[List[int]] = sizeIds
        self.colorIds: Optional[List[str]] = colorIds
        self.prices: Optional[List[int]] = prices
        self.skuIds: List[int] = skuIds  # уникальный
        self.spuId: int = spuId # общий
        self.floor_price: Optional[int] = floor_price
        self.all_images: List[str] = all_images
        self.brand: str = brand
        self.brand_logo: str = brand_logo
        self.title: str = title
        self.desc: Optional[str]= desc

    @classmethod
    def parse_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)
        skus = []
        current_colors = []
        current_sizes = []
        prices = []
        sizeIds = []
        colorIds = []
        for i in raw_data.skus:
            skus.append(i['skuId'])
            if 'price' in i:
                prices.append(i["price"]["prices"][0]["price"] if i["price"]["prices"] else 0)
            for j in i["properties"]:
                if 'saleProperty' in j:
                    if j["saleProperty"]["name"] == "颜色":
                        current_colors.append(j["saleProperty"]["value"])
                        colorIds.append(j["saleProperty"]["propertyValueId"])
                    elif j["saleProperty"]["name"] == "尺码":
                        current_sizes.append(j["saleProperty"]["value"])
                        sizeIds.append(j["saleProperty"]["propertyValueId"])

        all_images = [d["url"] for d in raw_data.image["spuImage"]["images"]]
        return cls(
            category=raw_data.detail["categoryName"],
            current_sizes=current_sizes,
            current_colors=current_colors,
            sizeIds=sizeIds,
            colorIds=colorIds,
            prices=prices,
            skuIds=skus,
            spuId=raw_data.detail["spuId"],
            floor_price=raw_data.price["item"]["floorPrice"] if raw_data.price else None,
            all_images=all_images, brand=raw_data.brandRootInfo["brandItemList"][0]["brandName"],
            brand_logo = raw_data.brandRootInfo["brandItemList"][0]["brandLogo"],
            title = raw_data.detail["title"], desc = raw_data.detail["desc"]
        )


if (__name__ == "__main__"):
    with open('new.json', 'r') as f:
        dictData = json.load(f)

    a = PoizonProduct.parse_json(json_data=dictData)
    print(f"sizeIDs = {a.sizeIds}")
    print(f"colorIds = {a.colorIds}")
    print(f"skuIds = {a.skuIds}")
    print(f"current_sizes = {a.current_sizes}")
    print(f"current_colors = {a.current_colors}")
    print(f"prices = {a.prices}\n")


    print(f"brand = {a.brand}")
    print(f"spuId = {a.spuId}")
    print(f"floor_price = {a.floor_price}")
    print(f"brand_logo = {a.brand_logo}")
    print(f"title = {a.title}")
    print(f"desc = {a.desc}")
    print(f"all_images = {a.all_images}")
    print(f"category = {a.category}")


