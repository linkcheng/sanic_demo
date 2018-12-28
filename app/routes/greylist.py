#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import logging
from sanic import Blueprint
from sanic.response import json

logger = logging.getLogger(__name__)
greylist_pb = Blueprint("greylist")


@greylist_pb.route("/grey_list_rank")
async def grey_list_rank(request):
    """
    灰名单等级。仅支持 GET 方法
    parameters:
      - id_card_number: str
      - mobile: str
      - decision_time: str
    responses:
      成功有数据: {"code": 0, "data": {"rank": 1}}
      成功但没有数据: {"code": 0, "data": null}
    """
    if request.method == "GET":
        req_json = request.json
        logger.info(f"request.json={req_json}")
        if not req_json:
            return json({"code": 1, "msg": "Only support Content-Type:application/json !"})

        id_card_number = req_json.get("id_card_number")
        mobile = req_json.get("mobile")
        decision_time = req_json.get("decision_time")

        db = request.app.db
        sql = f"""select rank from GreyList where id_card_number=%s 
            and mobile=%s and decision_time=%s;"""
        data = await db.get(sql, id_card_number, mobile, decision_time)

        logger.info(f"request.json={req_json}, response data={data}")
        return json({"code": 0, "data": data})
    else:
        return json({"code": 2, "msg": "Only support get method !"})
