import sys

import datetime
import numpy as np
import time
import pygame
import argparse

import random
from shapely.geometry import Polygon, Point


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def create_border(xlim, y_lim, border_type=None):
    if border_type is None:
        # if no argument is given just create a pretty looking triangle
        point1 = np.array([xlim[0] + 50, y_lim[1]-50])
        point2 = np.array([xlim[1] - 50, y_lim[1]-50])
        point3 = np.array([(point1[0]+point2[0])/2, y_lim[0]+50])
        return [point1, point2, point3]

    elif border_type == 'random_tri':
        # create random triangle
        point1 = np.array([np.random.randint(xlim[0], xlim[1]), np.random.randint(y_lim[0], y_lim[1])])
        point2 = np.array([np.random.randint(xlim[0], xlim[1]), np.random.randint(y_lim[0], y_lim[1])])
        point3 = np.array([np.random.randint(xlim[0], xlim[1]), np.random.randint(y_lim[0], y_lim[1])])
        return [point1, point2, point3]

    elif border_type == 'pentagon':
        point1 = np.array([xlim[0] + 100, y_lim[1] - 50])
        point2 = np.array([xlim[1] - 100, y_lim[1] - 50])
        point3 = np.array([(point1[0]+point2[0])/2, y_lim[0]+50])
        point4 = np.array([xlim[0] + 50, y_lim[0] + 200])
        point5 = np.array([xlim[1] - 50, y_lim[0] + 200])
        return [point1, point2, point3, point4, point5]

    print('USAGE: Bad border type given')
    sys.exit()


def random_point_in_triangle(A, B, C):
    # https://math.stackexchange.com/questions/18686/uniform-random-point-in-triangle-in-3d
    r1 = np.random.uniform(0,1)
    r2 = np.random.uniform(0,1)
    P = (1-np.sqrt(r1))*A + (np.sqrt(r1)*(1-r2))*B + (r2*np.sqrt(r1))*C
    return P


def get_random_point_in_polygon(border_points):
    # create the poly object
    poly = []
    for p in border_points:
        poly.append(tuple(p))

    # find a point in the poly
    point = Polygon(poly).representative_point().coords.xy
    point = np.array([point[0][0], point[1][0]])
    return point


def draw_point(surface, coord, color=BLACK, radius=2):
    pygame.draw.circle(surface, color, (coord[0], coord[1]), radius)


def calculate_halfway(p1, p2, dist_type='euclid'):
    if dist_type == 'euclid':
        point = (p1+p2)/2
        return point
    else:
        vector = p2-p1
        point = p1+(vector/1.001)
        return point


def draw_status(screen, font, i):
    pygame.draw.rect(screen, WHITE, (0, 0, 75, 25))
    font_surface = font.render(f"i = {i}", True, BLACK)
    screen.blit(font_surface, (5, 5))


def main(args):
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Sierpinski Triangle")
    screen.fill(WHITE)
    pygame.display.flip()

    # set up iteration counter
    font = pygame.font.Font(None, 20)

    # set up border shape
    border_points = create_border((0, 500), (0, 500), border_type=args.border_type)
    for p in border_points:
        draw_point(screen, p, RED)

    # get random point within border
    point = get_random_point_in_polygon(border_points)
    draw_point(screen, point, RED)

    i = 0
    running = True
    while running:
        draw_status(screen, font, i)
        pygame.display.update()

        j = np.random.randint(0, len(border_points))
        point = calculate_halfway(point, border_points[j], dist_type=args.dist_type)
        draw_point(screen, point, BLACK)

        # check if user quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        i += 1
        time.sleep(args.sleep)
        if args.max_iter != -1 and i >= args.max_iter:
            running = False

    # save final state if given
    if args.save_fn is not None:
        pygame.image.save(screen, args.save_fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CS 420/CS 527: Neuroevolution")
    parser.add_argument("--border_type", type=str, help="Type of border", default=None)
    parser.add_argument("--dist_type", type=str, help="Type of distance", default='euclid')
    parser.add_argument("--sleep", type=float, help="Duration of sleep", default=0.05)
    parser.add_argument("--max_iter", type=float, help="Maximum number of iterations", default=5000)
    parser.add_argument("--save_fn", type=str, help="Filename to save final state to", default=None)
    args = parser.parse_args()
    main(args)
