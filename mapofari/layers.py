#!/usr/bin/env python


from mapofari.errors import MapofariError
from mapofari.drivers import PostGIS, Shape
import sys
import pprint
import traceback
import yaml
try:
    import json
except ImportError:
    import simplejson as json


class Layers(object):

    drivers = {}

    def __init__(self, config, data, ignore_errors=True):
        self.data = data
        self.config = config
        self._layers = {}
        for name, info in self.data.iteritems():
            try:
                self._layers[name] = self.drivers[info['driver']](config, info)
            except Exception:
                if ignore_errors:
                    print "Can't create layer %s." % name
                    traceback.print_exc()
                else:
                    raise Exception

    def __setitem__(self, key, value):
        self._layers[key] = value

    def __getitem__(self, key):
        return self._layers[key]

    def __delitem__(self, key):
        del self._layers[key]

    def __iter__(self):
        return iter(self._layers)

    @classmethod
    def from_json(cls, config, data):
        data = json.loads(data)
        return cls(config, data)

    @classmethod
    def from_yaml(cls, config, data):
        data = yaml.load(data)
        return cls(config, data)

    @classmethod
    def from_xml(cls, config, data):
        raise NotImplementedError

    @classmethod
    def register(cls, driver):
        cls.drivers[driver.name] = driver

    def values(self):
        return self._layers.values()

    def items(self):
        return self._layers.items()
