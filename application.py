
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

from flask import Flask, render_template

app = Flask(__name__)

tablesvc = TableService(
    account_name='peebleslab',
    account_key='OxJE48VceGS4brzmrSwRwcUo3vB+q6cu+nt4I4elzlmEIcqxf28JLesGb8Qkb4060isc0MIESgcjP2H1HYIIKA==')

def comicinfo(comic_id):
    rowkey = str(comic_id).zfill(4)
    entities = tablesvc.query_entities('comics', filter=f"PartitionKey eq 'comics' and RowKey eq '{rowkey}'")
    return next(iter(entities))

def maxcomicid():
    rows = tablesvc.query_entities('comics', filter=f"PartitionKey eq 'global' and RowKey eq 'global'")
    row = next(iter(rows))
    return int(row.maxcomic)

@app.route("/<int:comic_id>")
def comic(comic_id):
    return render_template('comic.html', info=comicinfo(comic_id))

@app.route("/")
def hello():
    return comic(maxcomicid())
