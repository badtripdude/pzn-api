from .base import JsonSerializable
from typing import List, Dict, Optional
from .base import NON_STATED
# todo add param that diff prodDetail and prodDetailWithPrice
class PoizonProductRaw(JsonSerializable):
    """
        получение сырых данных с пойзона (практически сырой json)

    """
    def __init__(self,
                 price: Dict,
                 detail: Dict,
                 frontLabelSummaryDTO: Dict,
                 lastSold: Dict | NON_STATED,
                 image: Dict ,
                 spuGroupList: Dict | NON_STATED,
                 saleProperties: Dict | NON_STATED,
                 basicParam: Dict,
                 favoriteData: Dict,
                 brandRootInfo: Dict | NON_STATED,
                 sizeDto: Dict | NON_STATED,
                 relateProductInfo: Dict | NON_STATED,
                 shareInfo: Dict | NON_STATED,
                 skus: List | NON_STATED):
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
    def from_json(cls, json_data: Dict):
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
