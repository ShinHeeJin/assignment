from .schema import ns
from .schema import PostDto
from .utils import merge_http_status_msges, _get_post_cache_key, delete_entity_view_cache
from app import cache
from app.services.post_services import PostService
from app.utils import get_response
from flask import abort
from flask_restx import Resource
from http import HTTPStatus


@ns.route("/create")
class Post(Resource):
    @ns.doc(
        responses={
            200: ("Success", PostDto.base_response),
            400: merge_http_status_msges(
                [
                    "Validation Error (name)",
                    "Validation Error (content)",
                    "Validation Error (Invalid key)",
                ]
            ),
        },
        description="API to create Post",
        body=PostDto.post_create_req,
    )
    def post(self):
        result = PostService().create(ns.payload)
        return get_response(result, status_code=HTTPStatus.OK)


@ns.route("/<int:post_id>")
@ns.doc(responses={404: "Post not found"})
class PostItem(Resource):
    @cache.cached(timeout=60 * 60 * 24, make_cache_key=_get_post_cache_key)
    @ns.doc(
        params={"post_id": "POST DB PrimaryKey"},
        responses={200: ("Success", PostDto.post_get_res)},
        description="API to get Post information ( cf. The cache has been applied and will be updated upon modifying the entity. )",
    )
    def get(self, post_id):
        post = PostService().find_by_id(post_id)
        if not post:
            abort(HTTPStatus.NOT_FOUND, f"Post({post_id}) not found")
        return get_response(post, status_code=HTTPStatus.OK)

    @ns.doc(params={"post_id": "POST DB PrimaryKey"})
    @ns.doc(
        responses={
            204: ("Success ( No content )", PostDto.base_response),
            400: merge_http_status_msges(
                [
                    "Validation Error (name)",
                    "Validation Error (content)",
                    "Validation Error (Invalid key)",
                ]
            ),
        },
        description="API to update Post information ( Asynchronous API )",
        body=PostDto.post_update_req,
    )
    @delete_entity_view_cache("post")
    def put(self, post_id):
        result = PostService().update(post_id, ns.payload)
        if not result:
            abort(HTTPStatus.NOT_FOUND, f"Post({post_id}) not found")
        return get_response(status_code=HTTPStatus.NO_CONTENT)

    @ns.doc(
        params={"post_id": "POST DB PrimaryKey"},
        responses={
            204: ("Success ( No content )", PostDto.base_response),
        },
        description="API to delete Post information",
    )
    @delete_entity_view_cache("post")
    def delete(self, post_id):
        result = PostService().delete(post_id)
        if not result:
            abort(HTTPStatus.NOT_FOUND, f"Post({post_id}) not found")
        return get_response(status_code=HTTPStatus.NO_CONTENT)
