import uvicorn

from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from models import Assets,UserData
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesarcrud = CaesarCRUD()
maturityjwt = CaesarJWT(caesarcrud)
caesarcreatetables = CaesarCreateTables()
caesarcreatetables.create(caesarcrud)

JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAI Template. Hello"
@app.post("/api/save-risk-profile")
async def save_riskprofile(userData:UserData):
    risk_profile_exists = caesarcrud.check_exists(("*"), UserData.USERDATATABLE)
    if not risk_profile_exists:
         caesarcrud.post_data(fields=UserData.USERDATAFIELDNAME, values=(userData.riskProfile,), table=UserData.USERDATATABLE)
         return {"message":"risk profile was stored."}
    else:
        risk_profile = UserData(**caesarcrud.get_data(UserData.USERDATAFIELDNAME,UserData.USERDATATABLE)[0])
        caesarcrud.update_data(UserData.USERDATAFIELDNAME, values=(userData.riskProfile,), table=UserData.USERDATATABLE, condition=f"riskProfile = '{risk_profile.riskProfile}'")
        return {"message":"risk profile was updated."}

@app.get('/api/get-risk-profile')# GET # allow all origins all methods.
async def get_risk_profile():
    try:
        risk_profile_exists = caesarcrud.check_exists(("*"), UserData.USERDATATABLE)
        if not risk_profile_exists:
            return {"message":"No risk profile table found. Please create the table first."}
        else:
            risk_profile = caesarcrud.get_data(fields=UserData.USERDATAFIELDNAME, table=UserData.USERDATATABLE)[0]
            return risk_profile
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}



@app.post('/api/save-assets')# GET # allow all origins all methods.
async def save_assets(assets:Assets):
    try:
        completed = 0
        for asset in assets.assets:
            # Convert each asset to a tuple of values
            asset_tuple = (asset.name, asset.value, asset.type, asset.riskProfile, asset.pot, asset.id)
            # Post the data to the database
            asset_exists = caesarcrud.check_exists(("*"), Assets.ASSETSTABLE, f"name = '{asset.name}'")
            if not asset_exists:
                caesarcrud.post_data(fields=Assets.ASSETSFIELDNAME, values=asset_tuple, table=Assets.ASSETSTABLE)
            else:
                # If the asset already exists, you might want to update it instead
                caesarcrud.update_data(Assets.ASSETSFIELDNAME, values=asset_tuple, table=Assets.ASSETSTABLE, condition=f"name = '{asset.name}'")
            completed += 1
        return {"message":f"Successfully stored {completed} assets."}

    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/get-assets')# GET # allow all origins all methods.
async def get_assets():
    try:
        asset_exists = caesarcrud.check_exists(("*"), Assets.ASSETSTABLE)
        if not asset_exists:
            return {"message":"No assets table found. Please create the table first."}
        else:
            assets = caesarcrud.get_data(fields=Assets.ASSETSFIELDNAME, table=Assets.ASSETSTABLE)
            return {"assets":assets}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.delete('/api/delete-asset')# GET # allow all origins all methods.
async def delete_asset(id:str):
    try:
        asset_exists =  caesarcrud.check_exists(("*"), Assets.ASSETSTABLE,f"id = '{id}'")
        if asset_exists:
            caesarcrud.delete_data(Assets.ASSETSTABLE,f"id = '{id}'")
            return {"message":f"Asset ID {id} deleted."}
        else:
            return {"message":"Asset ID does not exist."}

    except Exception as ex:
        return {"error": f"{type(ex)},{ex}"}
@app.post('/api/save-timeline-data')# GET # allow all origins all methods.
async def save_timeline_data(timeline_data:JSONStructure):
    try:
        # Assuming timeline_data is a list of dictionaries
        if isinstance(timeline_data, list):
            for data in timeline_data:
                # Convert each dictionary to a tuple of values
                data_tuple = tuple(data.values())
                # Post the data to the database
                caesarcrud.post_data(fields=tuple(data.keys()), values=data_tuple, table="timeline")
            return {"message": "Successfully stored timeline data."}
        else:
            return {"error": "Invalid data format. Expected a list of dictionaries."}
    except Exception as ex:
        return {"error": f"{type(ex)},{ex}"}


if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
