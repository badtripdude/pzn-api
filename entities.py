import json


# parsing from json into ProductContainer lass
class ProductContainer:
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
