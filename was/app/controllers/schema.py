from flask_restx import Namespace, fields

ns = Namespace("post", description="POST CRUD API", expand="full")


class PostDto:
    base_response = ns.model(
        "base_response",
        {
            "data": fields.String(description="Any result data requested", example={}),
            "result": fields.Nested(
                ns.model(
                    "result",
                    {
                        "msg": fields.String(description="Response Reference msg", default=""),
                        "req_uuid": fields.String(
                            description="Request unique UUID",
                            default="e97a1a30920143bb9d8163f13867892d",
                        ),
                    },
                ),
                description="Default Api Response Format",
            ),
        },
    )

    post_create_req = ns.model(
        "post_create_req",
        {
            "name": fields.String(description="Post author name", example="John", required=True),
            "content": fields.String(
                description="Post content", example="something", required=True
            ),
        },
    )

    post_get_res = ns.inherit(
        "post_get_res",
        base_response,
        {
            "data": fields.Nested(
                ns.model(
                    "post_get_res_sub",
                    {
                        "id": fields.Integer(
                            description="Post Pirmary Key", example=1, required=False
                        ),
                        "name": fields.String(
                            description="Post name to update (no required)", required=False
                        ),
                        "content": fields.String(
                            description="Post content to update (no required)", required=False
                        ),
                        "created": fields.DateTime(
                            description="Post createion datetime",
                            example="2023-11-12 12:30:30",
                            required=False,
                        ),
                    },
                ),
                example={
                    "id": 1,
                    "name": "John",
                    "content": "anythnig",
                    "created": "2023-11-12 12:30:30",
                },
            )
        },
    )

    post_update_req = ns.model(
        "post_update_req",
        {
            "name": fields.String(
                description="Post name to update (no required)", example="Alice", required=False
            ),
            "content": fields.String(
                description="Post content to update (no required)",
                example="anything",
                required=False,
            ),
        },
    )
