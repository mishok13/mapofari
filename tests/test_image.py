#!/usr/bin/env python



import nose
from mapofari.image import Image



def test_line():
    image = Image(200, 200)
    image.line([(0,0), (200, 200)], (128, 256, 0), 10)
    print image.bytes()


def test_point():
    pass



def test_text_on_straight_line():
    pass



def test_text_on_curved_line():
    pass
n
