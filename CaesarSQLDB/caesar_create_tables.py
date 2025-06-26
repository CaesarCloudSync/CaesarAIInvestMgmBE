from CaesarSQLDB.caesarcrud import CaesarCRUD
from models.Assets import Assets
class CaesarCreateTables:
    def __init__(self) -> None:
        pass
    def create(self,caesarcrud :CaesarCRUD):
        caesarcrud.create_table(Assets.PRIMARYKEY,Assets.ASSETSFIELDNAME,
        Assets.ASSETSDATATYPES,Assets.ASSETSTABLE)