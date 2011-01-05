#!/usr/bin/env python

from .image import Image
import pyproj

def render(rules, layers):
    img = Image()
    for layer in layers:
        data = layer.data()
        for rule in layers.rules:
            img.draw(data, rules[rule])
    raise NotImplementedError


def reproject():
   raise NotImplementedError


def main():
    pass

if __name__ == '__main__':
    main()
