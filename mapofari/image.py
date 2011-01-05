#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cairo
import math
import functools
import time


class Image(object):

    formats = {'RGB32': cairo.FORMAT_ARGB32,
               'RGB24': cairo.FORMAT_RGB24,
               'A8': cairo.FORMAT_A8,
               'A1': cairo.FORMAT_A1}

    def __init__(self, width, height, fmt, background):
        try:
            cairo_format = self.formats[fmt.upper()]
        except KeyError:
            raise ValueError('Unknown image format')
        self.surface = cairo.ImageSurface(cairo_format, width, height)
        self.context = cairo.Context(self.surface)
        self.context.rectangle(0, 0, width, height)
        self.context.set_source_rgba(*background)
        self.context.fill()

    def line(self, points, color, width,
             dash=None, opacity=None, cap=None, join=None):
        """Draw a (multi)line on the image"""
        self.context.set_line_width(width)
        self.context.set_source_rgba(*color)
        start = points.pop(0)
        self.context.move_to(*start)
        for point in points:
            self.context.line_to(*point)
        self.context.stroke()

    def closed_line(self, points, color, width):
        """Draw a closed line"""
        self.context.set_line_width(width)
        self.context.set_source_rgba(*color)
        start = points.pop(0)
        self.context.move_to(*start)
        for point in points:
            self.context.line_to(*point)
        self.context.close_path()
        self.context.stroke()

    def polygon(self, points, color, width):
        """Draw a polygon"""
        self.context.set_line_width(width)
        self.context.set_source_rgba(*color)
        start = points.pop(0)
        self.context.move_to(*start)
        for point in points:
            self.context.line_to(*point)
        self.context.close_path()
        self.context.fill()

    def text(self, content, points, color, font='sans', size=14):
        start = points.pop(0)
        self.context.move_to(*start)
        self.context.select_font_face(font)
        self.context.set_font_size(size)
        self.context.set_source_rgba(*color)
        self.context.text_path(content)
        warp_path(self.context, functools.partial(angled, -0.3, start))
        self.context.fill()

    def angled_text(self, start, angle, text,
                    color=(0.0, 0.0, 0.0, 1.0), font='sans', size=14):
        # TODO: this is quite stupid and should be
        # improved by using pangocairo
        # TODO: or switch to freetype2 directly
        func = functools.partial(angled, -angle, start)
        self.context.move_to(*start)
        self.context.select_font_face(font)
        self.context.set_font_size(size)
        self.context.set_source_rgba(*color)
        self.context.text_path(text)
        warp_path(self.context, func)
        self.context.fill()

    def save(self, path):
        self.surface.write_to_png(path)


def warp_path(ctx, func):
    first = True
    for action, points in ctx.copy_path():
        if action == cairo.PATH_MOVE_TO:
            if first:
                ctx.new_path()
                first = False
            x, y = func(*points)
            ctx.move_to(x, y)
        elif action == cairo.PATH_LINE_TO:
            x, y = func(*points)
            ctx.line_to(x, y)
        elif action == cairo.PATH_CURVE_TO:
            x1, y1, x2, y2, x3, y3 = points
            x1, y1 = func(x1, y1)
            x2, y2 = func(x2, y2)
            x3, y3 = func(x3, y3)
            ctx.curve_to(x1, y1, x2, y2, x3, y3)
        elif action == cairo.PATH_CLOSE_PATH:
            ctx.close_path()


def angled(angle, start, x, y):
    xs, ys = start
    xw = xs + (x - xs) * math.cos(angle)
    yw = y + (xw - xs) * math.sin(angle)
    return xw - (y - ys) * math.sin(angle), yw


if __name__ == '__main__':
    im = Image(1000, 750, 'RGB32', (1.0, 1.0, 1.0, 1.0))
    im.line([(10, 40), (300, 400), (700, 200)], (0.0, 1.0, 1.0, 0.5), 10)
    im.closed_line([(50, 200), (100, 500), (750, 550)], (0.0, 0.0, 1.0, 0.5), 10)
    im.polygon([(140, 140), (500, 400), (700, 300)], (1.0, 0.0, 1.0, 0.5), 10)
    im.text(u'IiЁё', [(300, 300), (200, 400)], (0.1, 0.1, 0.1, 0.5), size=24)
    im.angled_text((200, 200), 0.25, 'Angled text', size=8, font='Envy Code R')
    im.save('/tmp/test.png')
