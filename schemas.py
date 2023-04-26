from marshmallow import Schema, fields


class PlainTodoSchema(Schema):
    todo_id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    status = fields.Str(required=True)


class TodoUpdateSchema(Schema):
    title = fields.Str()
    status = fields.Str()


class TodoSchema(PlainTodoSchema):
    user_id = fields.Int(required=False, load_only=True)
    user = fields.Nested(PlainTodoSchema(), dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserSchema(PlainUserSchema):
    todo = fields.List(fields.Nested(PlainTodoSchema()), dump_only=True)