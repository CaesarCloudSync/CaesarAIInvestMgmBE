from pydantic import BaseModel, Field
from typing import Optional, Dict, Any,List,ClassVar


class UserData(BaseModel):

    PRIMARYKEY:ClassVar[str] = "userdata_id"
    USERDATATABLE:ClassVar[tuple]  = "cii_invest_userdata"
    USERDATAFIELDNAME:ClassVar[tuple] = ("riskProfile",)
    USERDATADATATYPES:ClassVar[tuple] = ("varchar(255) NOT NULL",)
    riskProfile:str