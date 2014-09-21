class DictSerializer(object):
    _classes = []

    def dump(self, obj):
        if isinstance(obj, list):
            return [self.dump(x) for x in obj]
        if isinstance(obj, dict):
            return dict([(k, self.dump(v)) for k, v in obj.iteritems()])
        classnames = dict([(value, key) for key, value in self._classes])
        _class = classnames.get(type(obj), None)
        if _class:
            try:
                dump_method = getattr(self, 'dump_%s' % _class)
                return dump_method(obj)
            except AttributeError:
                data = dict(_class=_class)
                for key, value in obj.__dict__.iteritems():
                    data[key] = self.dump(value)
                return data
        return obj

    def load(self, obj):
        # print '------------'
        # print obj
        if isinstance(obj, list):
            return [self.load(x) for x in obj]
        if isinstance(obj, dict):
            try:
                _class = dict(self._classes)[obj.pop('_class')]
            except KeyError:
                _class = None
            data = dict()
            for key, value in obj.iteritems():
                data[key] = self.load(value)
            if _class:
                return _class(**data)
            return data
        return obj
