from base import JsonSerializable
from typing import List, Dict, Optional


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
