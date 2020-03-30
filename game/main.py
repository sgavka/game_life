"""
File with main classes with logic of game.

todo: create unit tests
"""
import random
from typing import Dict, Any


class World:
    """
    Main class for all logic classes.

    Word coordinates start from NW.
    """

    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.cells = []
        for x in range(self.width):
            tmp = []
            for y in range(self.height):
                tmp.append(None)
            self.cells.append(tmp)

    def set_cell(self, x: int, y: int, cell):
        """

        :param x:
        :param y:
        :param cell:
        """
        self.cells[x][y] = cell

    def get_cell(self, x, y):
        """

        :param x:
        :param y:
        :return:
        """
        if 0 <= x < self.width and 0 <= y < self.height:  # todo: check if width and height is inclusive
            return self.cells[x][y]
        else:
            return None

    def do_step(self):
        """
        Need implementation.
        """
        raise Exception()

    def start(self, steps_count=None):
        """

        :param steps_count:
        """
        if steps_count is None:
            while True:
                self.do_step()
        else:
            for _ in range(steps_count):
                self.do_step()


class Unit:
    """
    Base class for all logic for units.
    """
    GENOME_LEN = 64
    GENOME_MIN_VALUE = 0
    GENOME_MAX_VALUE = 64

    GENOME_COMMANDS: Dict[str, str] = {}

    BODY_LEN = 32

    BODY_PARAMS: Dict[int, Any] = {}

    def __init__(self, world: World, x, y):
        self.world = world
        self.x = x
        self.y = y

        self.body = {}

        self.memory = []
        self.memory_len = 32

        self.genome = []
        self.genome_point = 0
        # fill genome with zeroes
        for _ in range(self.GENOME_LEN):
            self.genome.append(0)

    def increase_genome_pointer(self):
        """
        Increase genome pointer to next. Genome is cycled.
        """
        self.genome_point += 1
        if self.genome_point >= self.GENOME_LEN:
            self.genome_point = self.genome_point - self.GENOME_LEN - 1

    def generate_random_genome(self):
        """
        Fill genome with absolute random values.
        """
        self.genome = []
        for _ in range(self.GENOME_LEN):
            self.genome.append(random.randrange(self.GENOME_MAX_VALUE))

    def set_genome(self, genome):
        """

        :param genome:
        """
        self.genome = genome

    def mutate_genome(self, gen_diff_probability, probability: int):
        """
        Method to do some implementation on genome.
        Need implementation.
        :param gen_diff_probability:
        :param probability:
        """
        raise Exception()

    def call_genome_command(self, command, *args, **nargs):
        """

        :param command:
        :param args:
        :param nargs:
        """
        getattr(self, self.GENOME_COMMANDS[command])(*args, **nargs)

    def get_actual_gen(self):
        """

        :return:
        """
        return self.genome[self.genome_point]

    def do_step(self):
        """
        Run calculations of unit's step.

        Maybe need implementation.
        """
        command = self.get_actual_gen()
        self.call_genome_command(command)

    def do_on_step(self, unit: 'Unit'):
        """
        Implementation for action then some unit step on self.
        Need implementation.
        :param unit:
        """
        raise Exception()

    def get_next_genome_value(self, count_of_steps=1):
        """

        :param count_of_steps:
        :return:
        """
        if self.genome_point + count_of_steps >= self.GENOME_LEN:
            value = self.genome[self.genome_point - self.GENOME_LEN]
        else:
            value = self.genome[self.genome_point + count_of_steps]
        return value
