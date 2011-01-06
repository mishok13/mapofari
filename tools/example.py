#!/usr/bin/env python


import argparse
import sys
import traceback

from mapofari.layers import Layers
from mapofari.drivers import PostGIS, Shape
import time
from shapely import wkb


def process(args):
    try:
        config = {'dbport': '5432',
                  'table_prefix': 'planet_osm',
                  'dbhost': 'localhost',
                  'dblogin': 'osm',
                  'dbpassword': '',
                  'dbname': 'gis'}
        Layers.register(PostGIS)
        Layers.register(Shape)
        l = Layers.from_yaml(config, args.layers)
        def simple():
            for name, layer in l.items():
                for data in layer.get([(-0.25, 51), (0.25, 52)]):
                    raw_data = data[-1]
                    if isinstance(raw_data, str):
                        print wkb.loads(raw_data.decode('hex'))
                    elif isinstance(raw_data, buffer):
                        print wkb.loads(str(raw_data))
                    else:
                        print type(raw_data)
        start = time.time()
        simple()
        print time.time() - start
    except Exception:
        traceback.print_exc()
        return 2
    except BaseException:
        traceback.print_exc()
        return 1


def main(args):
    sys.exit(process(args))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('layers', type=argparse.FileType('r'))
    main(parser.parse_args())
