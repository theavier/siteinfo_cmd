from fastapi import FastAPI
from checkSiteWhois import whois_domain_items
from checkSiteCMS import whatis_items
from checkSiteStatus import add_statuscode
from whereis import whereis_items

app = FastAPI()

def prepare_var(item):
    return [{'url': item}]

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/whois")
async def api_whois(url: str):
    return whois_domain_items(prepare_var(url))

@app.get("/whatis")
async def api_whatis(url: str):
    return whatis_items(prepare_var(url))

@app.get("/whereis")
async def api_whereis(url: str):
    return whereis_items(prepare_var(url))

@app.get("/status")
async def api_status(url: str):
    return add_statuscode(prepare_var(url))



# to test api run
# uvicorn py_fastapi:app --reload