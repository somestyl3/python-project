import pygame, sys, random

# configuration
field = height, width = 400, 200


colors = [(255, 255, 255), #  white
          (0, 0, 0), # black
          (255, 0, 0), # red
          (0, 0, 153), # blue
          (0, 204, 0), # green
          (236, 230, 0), # yellow
          (204, 0, 204)] # purple

shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]]
]
