from CaesarSQLDB.caesarcrud import CaesarCRUD
from models import Assets,UserData
class CaesarCreateTables:
    def __init__(self) -> None:
        pass
    def create(self,caesarcrud :CaesarCRUD):
        caesarcrud.create_table(Assets.PRIMARYKEY,Assets.ASSETSFIELDNAME,
        Assets.ASSETSDATATYPES,Assets.ASSETSTABLE)
        caesarcrud.create_table(UserData.PRIMARYKEY,UserData.USERDATAFIELDNAME,
        UserData.USERDATADATATYPES,UserData.USERDATATABLE)