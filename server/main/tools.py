"""
useful tools for whole project
"""

from django.http.response import JsonResponse
from django.core.files.base import File
from django.views.decorators.cache import cache_page
from multimedia.models import Video, Audio, Picture, Article
import datetime
from django.conf import settings


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
        return attr
    elif hasattr(obj, "keys"):
        if exp in obj.keys():
            return obj[exp]
        else:
            return None
    return None


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
                "status": status,
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


class CacheMixin(object):
    cache_timeout = settings.CACHE_TIME

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(
            *args, **kwargs
        )


def get_media_class(media_type):
    media_dict = {
        "video": Video,
        "article": Article,
        "picture": Picture,
        "audio": Audio,
    }
    return media_dict.get(media_type)
