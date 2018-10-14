from azure.cosmosdb.table.tableservice import TableService
from datetime import datetime
from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)

tablesvc = TableService(
    account_name='peebleslab',
    account_key='OxJE48VceGS4brzmrSwRwcUo3vB+q6cu+nt4I4elzlmEIcqxf28JLesGb8Qkb4060isc0MIESgcjP2H1HYIIKA==')

def comicinfo(comic_id = None):
    rowkey = str(comic_id).zfill(4)
    entities = tablesvc.query_entities('comics', filter=f"PartitionKey eq 'comics' and RowKey eq '{rowkey}'")
    return next(iter(entities))

def comicsinfo():
    return iter(tablesvc.query_entities('comics', filter="PartitionKey eq 'comics'"))

def maxcomicid():
    if maxcomicid.value == None:
        rows = tablesvc.query_entities('comics', filter=f"PartitionKey eq 'global' and RowKey eq 'global'")
        row = next(iter(rows))
        maxcomicid.value = int(row.maxcomic)

    return maxcomicid.value

maxcomicid.value = None

def pickbanner():
    bannerid = randint(1, maxcomicid())
    bannerinfo = comicinfo(bannerid)
    return {
        'id': bannerid,
        'info': bannerinfo,
        'url': bannerinfo.banner,
    }

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

    now = datetime.now()
    keywords = ','.join((info.title + ' ' + info.alt).split(' '))

    return render_template('comic.html', info=info, nav=nav, banner=pickbanner(), now=now, keywords=keywords, url=request.url)

@app.route("/")
def home():
    return comic(maxcomicid())

@app.route("/archive")
def archive():
    return render_template('archive.html', info=comicsinfo(), banner=pickbanner(), now=datetime.now(), url=request.url)
