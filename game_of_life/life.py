"""Simulates Conway's Game of Life."""

import argparse
import os
import sys
import time
from copy import deepcopy
from random import randint

# Setup cmd line options
parser = argparse.ArgumentParser(description="Conway's game of life")
parser.add_argument('--no-loop',
                    action='store_true',
                    help='Whether to show only one state or keep looping')
parser.add_argument('--size',
                    type=int,
                    default=35,
                    help='Number of rows')
parser.add_argument('--configuration',
                    default='random',
                    help='Specific configuration as a starting point')
parser.add_argument('--interval',
                    default=0.02,
                    type=float,
                    help='Time interval between generations')

class Universe:
    def __init__(self, size = 35, configuration='random'):
        self.rows = size
        self.cols = size * 2
        if configuration == 'random' :
            self.state = self.random()
        elif configuration == 'glider' :
            self.state = self.glider()
        else:
            print(f'[ERROR]: Configuration {configuration} not supported')
            return

    def random(self):
        """Generate random starting configuration."""
        return [[randint(0,1) for _ in range(self.cols)] \
                for _ in range(self.rows)]

    def glider(self):
        """Generate the configuration for a glider."""
        temp = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        temp[0][-3] = 1
        temp[1][-3] = 1
        temp[1][-1] = 1
        temp[2][-3] = 1
        temp[2][-2] = 1
        return temp

    def _neighbors(self, r, c):
        """Get the neighbors of a cell at row r and column c."""
        all_possible = [(r-1, c-1),
                (r-1, c  ),
                (r-1, c+1),
                (r  , c-1),
                (r  , c+1),
                (r+1, c-1),
                (r+1, c  ),
                (r+1, c+1)
                ]

        actual = [(r,c) for (r,c) in all_possible \
                if (r>=0 and c>=0 and \
                r<self.rows and c<self.cols)]
        return [self.state[r][c] for r,c in actual]

    def element_next_state(self, row, col):
        """Get the state of the element at row and col in the next iteration."""
        alive = bool(self.state[row][col])
        neighbors_around = sum(self._neighbors(row,col))
        if alive:
            if neighbors_around == 2 or neighbors_around == 3:
                return 1
            else:
                return 0
        else:
            return 1 if neighbors_around == 3 else 0

    def next_state(self):
        """Get the next state of the universe."""
        temp = deepcopy(self.state)
        for row in range(self.rows):
            for col in range(self.cols):
                temp[row][col] = self.element_next_state(row,col)
        self.state = temp
        return self

def render(universe):
    """Print out the universe."""
    def print_row(row):
        for e in ['ı'] + row + ['ı']:
            print(' ' if e == 0 else ('■' if e == 1 else 'ı'), end='') 
        print()

    print('-' * (universe.cols+2))
    for row in universe.state:
        print_row(row)
    print('-' * (universe.cols+2))


if __name__ == '__main__':
    arguments = parser.parse_args(sys.argv[1:])
    universe = Universe(arguments.size, arguments.configuration)

    # Generation starts at zero
    generation = 0

    render(universe)
    print(f'Generation: {generation}')

    if not arguments.no_loop:
        os.system('clear')
        while True:
            render(universe.next_state())
            generation = generation + 1
            print(f'Generation: {generation}')
            time.sleep(arguments.interval)
            os.system('clear')
