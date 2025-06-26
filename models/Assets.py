from pydantic import BaseModel, Field
from typing import Optional, Dict, Any,List,ClassVar

class Asset(BaseModel):
    name:str
    value:int
    type:str 
    riskProfile:str
    pot:str 
    id:str 
class Assets(BaseModel):

    PRIMARYKEY:ClassVar[str] = "asset_id"
    ASSETSTABLE:ClassVar[tuple]  = "cii_invest_assets"
    ASSETSFIELDNAME:ClassVar[tuple] = ("name", "value", "type", "riskProfile", "pot", "id")
    ASSETSDATATYPES:ClassVar[tuple] = ("varchar(255) NOT NULL","INT NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL")
    assets: List[Asset]
    [
    {
        "name": "APPL",
        "value": 30,
        "type": "stock",
        "riskProfile": "balanced",
        "pot": "balanced",
        "id": "1750928831666"
    },
    {
        "name": "GOOGLE",
        "value": 40,
        "type": "stock",
        "riskProfile": "balanced",
        "pot": "balanced",
        "id": "1750928864190"
    }
]