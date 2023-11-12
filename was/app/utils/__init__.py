from http import HTTPStatus
from app import db
from flask import jsonify, g, make_response


def get_response(data={}, msg="", status_code=HTTPStatus.OK):
    """
    API 반환 함수
    """
    if status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        db.session.rollback()
    db.session.commit()
    db.session.close()

    req_uuid = getattr(g, "req_uuid", None)
    response = make_response(
        jsonify({"data": data, "result": {"msg": msg, "req_uuid": req_uuid}}),
        int(status_code),
    )
    response.headers["Content-Type"] = "application/json"
    return response
