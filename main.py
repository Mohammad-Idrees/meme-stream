import databases
import sqlalchemy
from sqlalchemy import desc

env = ""

if env == "prod":
    DATABASE_URL = "postgres://jdrtjodvlpqwzb:dfa206764cb5a8c5f7358f5ae86b1d42d77626fef59a335838d3ba8849b1bf45@ec2-52-7-168-69.compute-1.amazonaws.com:5432/d561hj4baemcv6"
else:
    DATABASE_URL = "postgresql://us:password@localhost/data"

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)

table = sqlalchemy.Table(
    "table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("caption", sqlalchemy.String(100)),
    sqlalchemy.Column("url", sqlalchemy.String(1000))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

metadata.create_all(engine)

from fastapi import FastAPI, Request, HTTPException
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from typing import List, Optional

app = FastAPI(docs_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class datain(BaseModel):
    name : str
    caption : str 
    url : str 

class dataout(BaseModel):
    id : str
    name : str
    caption : str 
    url : str 

class datapatch(BaseModel):
    caption: Optional[str] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/memes')
async def add_meme(d: datain):
    query = table.insert().values(
        name = d.name,
        caption = d.caption,
        url = d.url
    )
    record_id = await database.execute(query)
    return {"id": str(record_id)}

@app.get('/memes', response_model=List[dataout])
async def latest100():
    query = table.select().order_by(desc(table.c.id)).limit(100)
    get_all = await database.fetch_all(query)
    return get_all

@app.get('/data', response_model=List[dataout])
async def complete_database():
    query = table.select().order_by(desc(table.c.id))
    get_all = await database.fetch_all(query)
    return get_all

@app.get('/memes/{id}', response_model=dataout)
async def get_meme_by_id(id: int):
    query = table.select().where(table.c.id == id)
    row = await database.fetch_one(query)
    if row==None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**row}


@app.patch('/memes/{id}', response_model=dataout)
async def update_meme(id: int, d: datapatch):
    query = table.select().where(table.c.id == id)
    stored_item_data =  await database.fetch_one(query)
    if stored_item_data == None:
        raise HTTPException(status_code=404, detail="Item not found")
    if d.caption =="string" or d.caption == "":
        d.caption = stored_item_data["caption"]
    if d.url == "string" or d.url == "":
        d.url = stored_item_data["url"]
    query = table.update().where(table.c.id == id).values(
        name = stored_item_data["name"],
        caption = d.caption,
        url = d.url
    )
    await database.execute(query)
    query = table.select().where(table.c.id == id)
    row = await database.fetch_one(query)
    return {**row}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="XMEME",
        version="2.5.0",
        description="Custom OpenAPI SWAGGER",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://freepngimg.com/download/internet_meme/19-2-meme-transparent-png.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/swagger-ui/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title= "XMEME" + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
