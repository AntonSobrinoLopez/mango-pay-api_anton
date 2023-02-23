import six

from .signals import pre_save, post_save
from .utils import force_text, force_str
# from . import get_default_handler

class BaseApiModelMethods(object):
    def __init__(self, *args, **kwargs):
        self._data = self._meta.get_default_dict()
        self._handler = kwargs.pop('handler', None)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def handler(self):
        pass
        return self._handler # or get_default_handler()

    def __repr__(self):
        try:
            u = six.text_type(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return force_str('<%s: %s>' % (self.__class__.__name__, u))

    def __str__(self):
        if six.PY2 and hasattr(self, '__unicode__'):
            return force_text(self).encode('utf-8')

        return '%s object' % self.__class__.__name__

    def __eq__(self, other):
        return (other.__class__ == self.__class__ and
                self.get_pk() and
                other.get_pk() == self.get_pk())
                
class BaseApiModel(BaseApiModelMethods):

    def __getattr__(self, name):
        return object.__getattribute__(self, self._meta.api_names.get(name, name))

    def __setattr__(self, name, value):
        super(BaseApiModel, self).__setattr__(self._meta.api_names.get(name, name), value)

    def fixed_kwargs(self):
        return {}

    def save(self, handler=None, cls=None, idempotency_key=None):
        self._handler = handler or self.handler

        field_dict = dict(self._data)
        field_dict.update(self.get_field_dict())
        field_dict.pop(self._meta.pk_name)

        all_fields = self._meta.fields

        if cls is None:
            cls = self.__class__

        created = False

        pre_save.send(cls, instance=self)

        if self.get_pk():
            update = self.update(
                self.get_pk(),
                **field_dict
            )
            result = update.execute(self._handler)
        else:
            for k, v in all_fields.items():
                if v.required is True and field_dict[v.name] is None:
                    raise ValueError('Missing mandatory field: ' + v.name)

            insert = self.insert(idempotency_key=idempotency_key, **field_dict)
            result = insert.execute(self._handler)

            created = True

        post_save.send(cls, instance=self, created=created)

        for key, value in result.items():
            setattr(self, key, value)

        return result

    @classmethod
    def select(cls, *args, **kwargs):
        return True
        # return SelectQuery(cls, *args, **kwargs)
