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
    def __init__(self, sizes, skuIds, spuId, floor_price, imgs, brand, brand_logo, title, desc):
        self.sizes = sizes
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
        sizes = [d["value"]  for d in raw_data.saleProperties["list"] if (d["name"] == "尺码")]
        # for d in raw_data.saleProperties["list"]:
        #     if (d["name"] == "尺码"):
        #         sizes.append(d["value"])
        # for d in raw_data.skus:
        #     cls.skuIds.append(d["skuId"])
        skus = [d["skuId"] for d in raw_data.skus]
        spuId = raw_data.detail["spuId"]
        floor_price = raw_data.price["item"]["floorPrice"]
        # for i in raw_data.image["spuImage"]["images"]:
        #     cls.imgs.append(i["url"])
        imgs = [d["url"] for d in raw_data.image["spuImage"]["images"]]
        brand = raw_data.brandRootInfo["brandItemList"][0]["brandName"]
        brand_logo = raw_data.brandRootInfo["brandItemList"][0]["brandLogo"]
        title = raw_data.detail["title"]
        desc = raw_data.detail["desc"]
        return cls(
            sizes=sizes,
            skuIds=skus,
            spuId=spuId,
            floor_price=floor_price,
            imgs=imgs, brand=brand,
            brand_logo=brand_logo,
            title=title, desc=desc
        )


if (__name__ == "__main__"):
    with open('data.json', 'r') as f:
        dictData = json.load(f)
    a = PoizonProduct.parse_json(json_data=dictData)
    print(a.imgs)
# sizes = []
# propertyValueIds = []
# skus = []
# spu: int
# title: str
# # to get sizes
# for d in dictData["saleProperties"]["list"]:
#     if (d["name"] == "尺码"):
#         sizes.append(d["value"])
# # to get propertyValueId
# for d in dictData["saleProperties"]["list"]:
#     if (d["name"] == "尺码"):
#         propertyValueIds.append(d["propertyValueId"])
# # to get skus
# for d in dictData["skus"]:
#     skus.append(d["skuId"])
# # to get spuId
# spu = dictData["detail"]["spuId"]
#
# # to get title
# title = dictData["detail"]["title"]
#
# #to get desc
# desc = dictData["detail"]["desc"]
# #to get images
# images = []
# for i in dictData["image"]["spuImage"]["images"]:
#     images.append(i["url"])
#
# # to get brand logo and brand
# brand = dictData["brandRootInfo"]["brandItemList"][0]["brandName"]
# brand_logo = dictData["brandRootInfo"]["brandItemList"][0]["brandLogo"]
# print(f"sizes = {sizes}")
# print(propertyValueIds)
# print(f"skus_list = {skus}\n")
# print(f"spu = {spu}\n")
# print(f"title= {title}\n")
# print(f"desc= {desc}\n")
# print(f"brand= {brand}\n")
# print(f"brand_logo= {brand_logo}\n")
# print(f"imgs = {images}")
#
