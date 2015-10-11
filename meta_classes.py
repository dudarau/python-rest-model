from primitives import Typed
import requests
import json


def _post(self, **params):

    format_args = self.__dict__.pop('format_args') if 'format_args' in self.__dict__ else None

    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    endpoint = self.Meta.post.format(**format_args) if format_args else self.Meta.post
    self.format_args = None # this should be handled in a cleaner way
    self.__dict__ = {}
    return requests.post(endpoint, data=body)


def _put(self, **params):

    format_args = self.__dict__.pop('format_args') if 'format_args' in self.__dict__ else None

    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    endpoint = self.Meta.put.format(**format_args) if format_args else self.Meta.put
    self.format_args = None # this should be handled in a cleaner way
    self.__dict__ = {}
    return requests.put(endpoint, data=body)


def _delete(self, **params):
    format_args = self.__dict__.pop('format_args') if 'format_args' in self.__dict__ else None

    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)

    endpoint = self.Meta.delete.format(**format_args) if format_args else self.Meta.delete
    self.format_args = None # this should be handled in a cleaner way
    self.__dict__ = {}
    return requests.delete(endpoint, data=body)


def _get(self, **params):
    """if get has an id it should be used to retrieve a single item otherwise it would be retrieving a list"""

    format_args = self.__dict__.pop('format_args') if 'format_args' in self.__dict__ else None
    for k, v in params.items():
        setattr(self, k, v)

    body = json.dumps(self.__dict__)
    endpoint = self.Meta.get.format(**format_args) if format_args else self.Meta.get
    self.format_args = None # this should be handled in a cleaner way
    self.__dict__ = {}
    return requests.get(endpoint, data=body)

def _format(self, **format_args):
    self.format_args = format_args
    return self


class RestModelMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name

        new_class = type.__new__(cls, clsname, bases, clsdict)

        if clsname != "RestModel":
            if 'Meta' not in clsdict:
                raise Exception("Meta class must be provided")

            setattr(new_class, "format_args", None)
            setattr(new_class, "format", _format)
            if 'post' in clsdict['Meta'].__dict__:
                setattr(new_class, "post", _post)
            if 'put' in clsdict['Meta'].__dict__:
                setattr(new_class, "put", _put)
            if 'delete' in clsdict['Meta'].__dict__:
                setattr(new_class, "delete", _delete)
            if 'get' in clsdict['Meta'].__dict__:
                setattr(new_class, "get", _get)

        return new_class
