import json

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
        self.price = price
        self.detail = detail
        self.frontLabelSummaryDTO = frontLabelSummaryDTO
        self.lastSold = lastSold
        self.image = image
        self.spuGroupList = spuGroupList
        self.saleProperties = saleProperties
        self.basicParam = basicParam
        self.favoriteData = favoriteData
        self.brandRootInfo = brandRootInfo
        self.sizeDto = sizeDto
        self.relateProductInfo = relateProductInfo
        self.shareInfo = shareInfo
        self.skus = skus

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
    def __init__(self, sizes, colors, sizeIds, prices, skuIds, spuId, floor_price, imgs, brand, brand_logo, title, desc):

        self.sizes = sizes
        self.colors = colors
        self.sizeIds = sizeIds
        self.prices = prices
        self.skuIds = skuIds  # уникальный
        self.spuId = spuId # общий
        self.floor_price = floor_price
        self.imgs = imgs
        self.brand = brand
        self.brand_logo = brand_logo
        self.title = title
        self.desc = desc

    @classmethod
    def parse_json(cls, json_data):
        raw_data = PoizonProductRaw.from_json(json_data=json_data)

        if "saleProperty" in raw_data.skus[0]["properties"][1]:
            sizes = [d["properties"][1]["saleProperty"]["value"] for d in raw_data.skus]
        else: sizes = None

        colors = 0
        sizeIds = [d["propertyValueId"]  for d in raw_data.saleProperties["list"] if (d["name"] == "尺码")]
        prices = []
        if ("price" in raw_data.skus[0]):
            for d in raw_data.skus:
                if d["price"]["prices"]:
                    prices.append(d["price"]["prices"][0]["price"])
                else:
                    prices.append(0)
        else: prices = None
        skus = [d["skuId"] for d in raw_data.skus]
        spuId = raw_data.detail["spuId"]
        floor_price = raw_data.price["item"]["floorPrice"]
        imgs = [d["url"] for d in raw_data.image["spuImage"]["images"]]
        brand = raw_data.brandRootInfo["brandItemList"][0]["brandName"]
        brand_logo = raw_data.brandRootInfo["brandItemList"][0]["brandLogo"]
        title = raw_data.detail["title"]
        desc = raw_data.detail["desc"]
        return cls(
            sizes=sizes,
            colors=colors,
            sizeIds=sizeIds,
            prices=prices,
            skuIds=skus,
            spuId=spuId,
            floor_price=floor_price,
            imgs=imgs, brand=brand,
            brand_logo=brand_logo,
            title=title, desc=desc
        )


if (__name__ == "__main__"):
    with open('productDetailWithPrice.json', 'r') as f:
        dictData = json.load(f)

    a = PoizonProduct.parse_json(json_data=dictData)
    print(f"sizeIDs = {a.sizeIds}")
    print(f"skuIds = {a.skuIds}")
    print(f"sizes = {a.sizes}")
    print(f"prices = {a.prices}\n")


