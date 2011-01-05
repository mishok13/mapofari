#!/usr/bin/env python


from __future__ import with_statement


import psycopg2
from operator import itemgetter
import pyproj
import math


class BaseDriver(object):

    def __init__(self, config, info):
        self.srs = str(info.get('srs', "+proj=merc +datum=WGS84 +over"))
        self.projection = pyproj.Proj(self.srs)

    def get(self, bbox):
        raise NotImplementedError

    def get_async(self, bbox, callback):
        raise NotImplementedError

    def send(self, bbox):
        raise NotImplementedError

    def receive(self, bbox):
        raise NotImplementedError


class PostGIS(BaseDriver):

    name = 'postgis'

    def __init__(self, config, info):
        self.config = config
        self.query = info['query'] % config
        self.connection_info = info['connection']
        self.host = self.connection_info['host'] % config
        self.port = int(self.connection_info.get('port', '5432') % config)
        self.login = self.connection_info.get('login', '') % config
        self.password = self.connection_info.get('password', '') % config
        self.database = self.connection_info['database'] % config
        self.connection = psycopg2.connect(database=self.database,
                                           host=self.host,
                                           port=self.port,
                                           user=self.login,
                                           password=self.password)
        super(PostGIS, self).__init__(config, info)

    def get(self, bbox):
        bbox = self.projection(*bbox[0]), self.projection(*bbox[1])
        bbox = {'minx': min(map(itemgetter(0), bbox)),
                'miny': min(map(itemgetter(1), bbox)),
                'maxx': max(map(itemgetter(0), bbox)),
                'maxy': max(map(itemgetter(1), bbox))}
        width = bbox['maxx'] - bbox['minx']
        height = bbox['maxy'] - bbox['miny']
        zoom = 18 - int(math.log(max(width, height) / 1000, 2))
        bbox = "SetSRID('BOX3D(%(minx)s %(miny)s, %(maxx)s %(maxy)s)'::box3d, 900913)" % bbox
        query = self.query.replace('$zoom$', str(zoom)).replace('$bbox$', bbox)
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        return res


class Shape(BaseDriver):

    name = 'shape'

    def __init__(self, config, info=None):
        self.config = config
        self.info = info
        self.path = info['path']
        super(Shape, self).__init__(config, info)

    def _clip(self, shape):
        """Clip the geometry, so we don't overuse rendering power"""
        raise NotImplementedError

    def get(self, bbox):
        with open(self.path) as shape:
            return self._clip(shape.read())

    def send(self, bbox):
        """Shape plugin is disk-based, so we don't really need to be async"""
        pass

    def receive(self, bbox):
        return self.get(bbox)

    def get_async(self, bbox, callback):
        callback(self.get(bbox))
