from marshmallow import Schema, fields


class TodoSchema(Schema):
    todo_id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    status = fields.Str(required=True)


class TodoUpdateSchema(Schema):
    title = fields.Str()
    status = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
