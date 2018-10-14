from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from datetime import datetime
from flask import Flask, render_template
from random import randint

app = Flask(__name__)

tablesvc = TableService(
    account_name='peebleslab',
    account_key='OxJE48VceGS4brzmrSwRwcUo3vB+q6cu+nt4I4elzlmEIcqxf28JLesGb8Qkb4060isc0MIESgcjP2H1HYIIKA==')

def comicinfo(comic_id):
    rowkey = str(comic_id).zfill(4)
    entities = tablesvc.query_entities('comics', filter=f"PartitionKey eq 'comics' and RowKey eq '{rowkey}'")
    return next(iter(entities))

def maxcomicid():
    if maxcomicid.value == None:
        rows = tablesvc.query_entities('comics', filter=f"PartitionKey eq 'global' and RowKey eq 'global'")
        row = next(iter(rows))
        maxcomicid.value = int(row.maxcomic)

    return maxcomicid.value

maxcomicid.value = None

@app.route("/<int:comic_id>")
def comic(comic_id):
    comic_id = max(1, comic_id)
    comic_id = min(comic_id, maxcomicid())

    info = comicinfo(comic_id)

    nav = { 
        'first': 1,
        'prev': max(comic_id - 1, 1),
        'next': min(comic_id + 1, maxcomicid()),
        'last': maxcomicid(),
        'random': randint(1, maxcomicid()),
    }

    bannerid = randint(1, maxcomicid())
    bannerinfo = comicinfo(bannerid)
    banner = {
        'id': bannerid,
        'info': bannerinfo,
        'url': bannerinfo.banner,
    }

    now = datetime.now()

    return render_template('comic.html', info=info, nav=nav, banner=banner, now=now)

@app.route("/")
def home():
    return comic(maxcomicid())
