from flask import Blueprint, request, jsonify
from ModelServices.MemoService import MemoService
import json

memo_bp = Blueprint("memo_ctrl", __name__, url_prefix="/memo")


@memo_bp.route('', methods=["GET"])
def memo_controller():
    memo_service = MemoService()
    if request.method == 'GET':
        memo = memo_service.get_memo().first()
        res = {
            'id': memo[0].memo_id,
            'author': memo.name,
            'title': memo[0].title,
            'content': memo[0].content
        }
    json_res = json.dumps(res)
    return jsonify(code="0", data=json_res)
