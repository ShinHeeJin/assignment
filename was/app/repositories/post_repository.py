from .base_repository import BaseRepository
from app import db
from app.entities import Post
from app.schema.post_schema import PostSchema
from celery import shared_task
from flask import current_app
import time


class PostRepository(BaseRepository):
    def __init__(self):
        super().__init__(Post)

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @staticmethod
    @shared_task
    def _async_update(post_id, data):
        time.sleep(5)

        post = Post.query.get(post_id)
        updated = PostSchema(partial=True).load(data)
        updated.id = post.id
        db.session.merge(updated)
        db.session.commit()

    def _sync_update(self, post_id, data):
        post = self.get(post_id)
        updated = PostSchema(partial=True).load(data)
        updated.id = post.id
        db.session.merge(updated)
        db.session.commit()

    def update(self, post_id, data):
        if current_app.config["APP_CONFIG"] != "test":
            PostRepository._async_update.delay(post_id, data)
        else:
            self._sync_update(post_id, data)
        return True
