from netaddr import IPNetwork, IPAddress

BASE_CLASSES = (int, str, list, dict)


class DictSerializer(object):
    _classes = ()

    def dump(self, obj):
        if isinstance(obj, list):
            return [self.dump(x) for x in obj]
        if isinstance(obj, dict):
            return dict([(k, self.dump(v)) for k, v in obj.iteritems()])
        classnames = dict([(value, key) for key, value in self._classes])
        try:
            _class = classnames[type(obj)]
        except KeyError:
            if not isinstance(obj, BASE_CLASSES):
                raise
        data = dict()
        for key, value in obj.__dict__.iteritems():
            if isinstance(value, (list,)):
                try:
                    value = [self.dump(x) for x in value]
                except AttributeError:
                    pass
            if isinstance(value, (IPNetwork, IPAddress)):
                value = str(value)
            try:
                data[key] = value.dump()
            except AttributeError:
                data[key] = value
            data['_class'] = _class
        return data

    def load(self, data):
        try:
            _class = dict(self._classes)[data.pop('_class')]
        except TypeError:
            if isinstance(data, list):
                return [self.load(x) for x in data]
        except KeyError:
            if isinstance(data, dict):
                return dict([(k, self.load(v)) for k, v in data.iteritems()])
        attributes = dict()
        for key, value in data.iteritems():
            try:
                if '_class' in value.keys():
                    value = self.load(value)
            except AttributeError:
                pass
            if isinstance(value, (list,)):
                try:
                    value = [self.load(x) for x in value]
                except AttributeError:
                    pass
            attributes[key] = value
        return _class(**attributes)
