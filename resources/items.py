import uuid
from flask import abort, request
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on Items")

@blp.route("/item/<string:item_id>")
class ItemOperations(MethodView):
    @blp.response(200, ItemSchema)
    # return a paticular item
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, description="Item not found")
    
    # delete a paticular item
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"description": "Item deleted"}
        except KeyError:
            abort(404, description="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # update a paticular item
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404, description="Item not found")
        
@blp.route("/items")
class Items(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if item_data["name"] in item["name"]:
                abort(400, description="Item already exists")
        item_id = uuid.uuid4().hex
        item = {**item_data, "item_id": item_id}
        items[item_id] = item
        return item, 201