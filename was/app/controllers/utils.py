from app import cache
from flask import request


def _get_post_cache_key(*args, **kwargs):
    post_id = request.view_args.get("post_id")
    if not post_id:
        raise AttributeError("post_id not in kwargs")
    return f"post_{post_id}"


def delete_entity_view_cache(entity_name):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            idx_name = f"{entity_name}_id"
            idx = request.view_args.get(idx_name, None)
            if not idx:
                raise AttributeError(f"'{idx_name}' not in view_args")

            cache.delete(f"{entity_name}_{idx}")
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__

        return wrapper

    return decorated_func


def merge_http_status_msges(messages: list):
    """
    API Http status code description 메세지 병합
    Args:
        messages : list of str
    """
    result = ""
    for idx, message in enumerate(messages, 1):
        result += f" {idx}. {message}"
        if len(messages) != idx:
            result += "\n"
    return result
