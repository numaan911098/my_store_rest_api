from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PlainItemSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    item_id = fields.Str(dump_only=True)

class ItemUpdateSchema(Schema):
    price = fields.Float()
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    store_id = fields.Str(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema, dump_only=True) # this is a store object

class StoreSchema(PlainStoreSchema):
    items = fields.Nested(PlainItemSchema, dump_only=True)