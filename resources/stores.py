import uuid
from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores")

@blp.route("/store/<string:store_id>")
class StoreOperations(MethodView):
    @blp.response(200, StoreSchema)
    # return a paticular store
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, description="Store not found")
    
    # delete a paticular store
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"description": "Store deleted"}
        except KeyError:
            abort(404, description="Store not found")
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    
    # update a paticular store
    def put(self, store_data, store_id):
        try:
            store = stores[store_id]
            store |= store_data

            return store
        except KeyError:
            abort(404, description="Store not found")

@blp.route("/stores")
class Stores(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] in store["name"]:
                abort(400, description="Store already exists")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201