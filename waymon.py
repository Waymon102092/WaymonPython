from flask import jsonify
from sqlalchemy.orm import DeclarativeMeta
import requests
import json


def res(data=None, msg="ok", status=0):
    """
        json 返回值
    """
    response = {
        "data": data,
        "msg": msg,
        "status": status
    }
    try:
        response['data'] = serializer(data)
        return jsonify(response)
    except SerializationError as e:
        response['status'] = e.code
        response['msg'] = e.message
        return jsonify(response)


def serializer(obj):
    """
    将对象转换为可以序列化为JSON的数据类型
    """
    if obj is None:
        return None
    try:
        # 如果对象本身就是可以序列化为JSON的类型，则直接返回
        if isinstance(obj, (str, int, float, bool, list, tuple, dict)):
            return obj
        # 如果对象是ORM对象，则将其转换为字典并返回
        elif isinstance(obj.__class__, DeclarativeMeta):
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        # 如果对象实现了__dict__方法，则将其转换为字典并返回
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            raise SerializationError(code=500, message="Cannot serializer obj")
    except Exception as e:
        raise SerializationError(code=500, message=str(e))


class SerializationError(Exception):
    """
       自定义的异常类，用于处理序列化错误
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message


def get(uri, params):
    """
       get 请求
    """
    response = requests.get(uri, data=params)
    if response.status_code == 200:
        result = json.loads(response.content)
        return result
    else:
        return res(None, response.text, response.status_code)


def post(uri, data):
    """
        post 请求
    """
    response = requests.post(uri, json=data)
    if response.status_code == 200:
        result = json.loads(response.content)
        return result
    else:
        return res(None, response.text, response.status_code)


