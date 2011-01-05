#!/usr/bin/env python


import yaml
import sys
from pprint import pprint


class Style(object):

    def __init__(self, config, data):
        self.style = data

    def __repr__(self):
        return repr(self.style)

    def __str__(self):
        return str(self.style)

    @classmethod
    def from_xml(cls):
        raise NotImplementedError

    @classmethod
    def from_json(cls):
        raise NotImplementedError

    @classmethod
    def from_yaml(cls, config, data):
        data = yaml.load(data)
        return cls(config, data)


if __name__ == '__main__':
    style = Style.from_yaml(None, open(sys.argv[1]).read())
    pprint(style.style)
