from __future__ import division

import pygame
from math import pi
from random import random

from .arena import Arena, ARENA_MARKINGS_COLOR, ARENA_MARKINGS_WIDTH

from ..markers import Token
from ..vision import MARKER_TOKEN_A, MARKER_TOKEN_B, MARKER_TOKEN_C

def token_positions(separation1, separation2):
    """
    Iterate over a 3x3 grid of positions, centered at the middle of the arena
    and with the given separation.

    Positions are yielded top-to-bottom, left-to-right.
    """
    offsets = (-separation1, 0, separation1)
    for x_pos in offsets:
        for y_pos in offsets:
            yield x_pos, y_pos
        yield x_pos, -separation1-separation2
        yield x_pos, separation1+separation2
        yield -separation1-separation2, x_pos
        yield separation1+separation2, x_pos

class HillsRoadArena(Arena):
    start_locations = [( 0, -3),
                       ( 3,  0),
                       ( 0,  3),
                       (-3,  0)]

    start_headings = [0.5*pi,
                      pi,
                      -0.5*pi,
                      0]

    zone_size = 1

    def __init__(self, objects=None, wall_markers=True, num_tokens=5):
        super(HillsRoadArena, self).__init__(objects, wall_markers)

        positions = token_positions(0.75, 0.875)
        token_types = [
            (MARKER_TOKEN_A, 0),
            (MARKER_TOKEN_B, 0),
            (MARKER_TOKEN_A, 1),
            (MARKER_TOKEN_B, 1),
            (MARKER_TOKEN_C, 0),
            (MARKER_TOKEN_B, 2),
            (MARKER_TOKEN_A, 2),
            (MARKER_TOKEN_B, 3),
            (MARKER_TOKEN_A, 3),
            (MARKER_TOKEN_A, 0),
            (MARKER_TOKEN_B, 0),
            (MARKER_TOKEN_A, 1),
            (MARKER_TOKEN_B, 1),
            (MARKER_TOKEN_C, 0),
            (MARKER_TOKEN_B, 2),
            (MARKER_TOKEN_A, 2),
            (MARKER_TOKEN_B, 3),
            (MARKER_TOKEN_A, 3),
            (MARKER_TOKEN_A, 2),
            (MARKER_TOKEN_B, 3),
            (MARKER_TOKEN_A, 3),
        ]

        for pos, (marker_type, offset) in zip(positions, token_types):
            token = Token(self, offset, damping=10, marker_type=marker_type)
            token.location = pos
            self.objects.append(token)

    def draw_background(self, surface, display):
        super(HillsRoadArena, self).draw_background(surface, display)

        # Corners of the inside square
        top_left     = display.to_pixel_coord((self.left + self.zone_size, self.top + self.zone_size), self)
        top_right    = display.to_pixel_coord((self.right - self.zone_size, self.top + self.zone_size), self)
        bottom_right = display.to_pixel_coord((self.right - self.zone_size, self.bottom - self.zone_size), self)
        bottom_left  = display.to_pixel_coord((self.left + self.zone_size, self.bottom - self.zone_size), self)

        # Lines separating zones
        def line(start, end):
            pygame.draw.line(surface, ARENA_MARKINGS_COLOR, \
                             start, end, ARENA_MARKINGS_WIDTH)

        line((0, 0), top_left)
        line((display.size[0], 0), top_right)
        line(display.size, bottom_right)
        line((0, display.size[1]), bottom_left)

        # Square separating zones from centre
        pygame.draw.polygon(surface, ARENA_MARKINGS_COLOR, \
                            [top_left, top_right, bottom_right, bottom_left], 2)
