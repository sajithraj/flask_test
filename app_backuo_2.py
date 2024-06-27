import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.get("/")
def hello():
    return "hello"


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def add_stores():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    pudhu_store = {** store_data, "store_id": store_id}
    stores[store_id] = pudhu_store
    return pudhu_store, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except Exception as e:
        print(e)
        abort(404, message="Store not found")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")


@app.get("/item")
def get_items():
    return {"items": list(items.values())}


@app.post("/item")
def add_items():
    item_data = request.get_json()
    print(item_data)
    print(stores)
    if ("name" not in item_data or "price" not in item_data or "store_id" not in item_data):
        abort(404, message="item did not have name or price or store_id.")

    if (item_data['store_id'] not in stores):
        abort(404, message="item not found.")

    item_id = uuid.uuid4().hex
    pudhu_item = {** item_data, "item_id": item_id}
    items[item_id] = pudhu_item
    return pudhu_item, 201


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # There's  more validation to do here!
    # Like making sure price is a number, and also both items are optional
    # You should also prevent keys that aren't 'price' or 'name' to be passed
    # Difficult to do with an if statement...
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except Exception as e:
        print(e)
        abort(404, message="item not found")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
