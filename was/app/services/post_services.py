from app.repositories.post_repository import PostRepository
from app.schema.post_schema import PostSchema


class PostService:
    def __init__(self):
        self.repository = PostRepository()
        self.schema = PostSchema

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def create(self, post_data):
        post = self.schema().load(post_data)
        post = self.repository.insert(post)
        return self.schema().dump(post) if post else None

    def find_by_id(self, post_id):
        if post_id <= 0:
            return None
        post = self.repository.get(post_id)
        if not post:
            return None
        return self.schema().dump(post)

    def update(self, post_id, data):
        post = self.repository.get(post_id)
        PostSchema(partial=True).load(data)
        if not post:
            return None
        return self.repository.update(post_id, data)

    def delete(self, post_id):
        post = self.repository.get(post_id)
        if not post:
            return None
        return self.repository.delete(post)
