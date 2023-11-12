from app.entities import Post
from datetime import datetime
from marshmallow import Schema, post_load, fields, pre_load
import base64


class PostSchema(Schema):
    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @post_load
    def to_object(self, data, **kwargs):
        content = data.get("content", None)
        if content:
            data["content"] = content.encode("utf-8")
        return Post(**data)

    id = fields.Integer(dump_only=True, allow_none=True)
    name = fields.String(required=True)
    content = fields.String(required=True)
    created = fields.DateTime(dump_only=True, default=datetime.now(), format="%Y-%m-%d %H:%M:%S")
