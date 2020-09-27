"""
useful tools for whole project
"""

from django.http.response import JsonResponse
from django.db.models import Model
from django.core.files.base import File
import datetime


def _evaluate(obj, exp):
    attr = obj
    if hasattr(obj, exp):
        attr = eval("obj." + exp)
        if "RelatedManager" in attr.__class__.__name__:
            return attr.all()
        elif callable(attr):
            return attr()
        elif isinstance(attr, File):
            return attr.url  # todo set staticfiles url for deployment
        elif isinstance(attr, datetime.datetime):
            return str(attr)
    elif hasattr(obj, "keys"):
        if exp in obj.keys():
            return obj[exp]
        else:
            return None
    return attr


def _serialize(data, _format, _maxlen={}):
    """
     Serialize data based on format to native python datatype
    :param data: dict object containing data to be serialized
    :param _format: format for the data to be serialized
    :param _maxlen: max length for a list
    :return: serialized data
    """
    serialized_data = {}
    for key in _format.keys():
        if _format[key] == 1:
            obj = _evaluate(data, key)
            serialized_data[key] = obj
        elif type(_format[key]) is dict:
            obj = _serialize(data[key], _format[key], _maxlen)
            serialized_data[key] = obj
        elif type(_format[key]) is list:
            real_list = _evaluate(data, key)
            if key in _maxlen.keys():
                real_list = real_list[: _maxlen[key]]
            iter_obj = []
            for i in real_list:
                obj = _serialize(i, _format[key][0], _maxlen)
                iter_obj.append(obj)
            serialized_data[key] = iter_obj
        else:
            serialized_data[key] = None
    return serialized_data


def return_response(
    status=True,
    response_data={},
    response_success=[],
    response_errors=[],
    format={},
    response_maxlen={},
):
    if format and response_data:
        response_data = _serialize(response_data, format, response_maxlen)
    print(response_data)
    try:
        return JsonResponse(
            {
                "status": True,
                "data": response_data,
                "errors": response_errors,
                "success": response_success,
            }
        )
    except:
        return JsonResponse(
            {
                "status:": False,
                "data": None,
                "errors": "Oops Something went wrong",
                "success": None,
            }
        )
