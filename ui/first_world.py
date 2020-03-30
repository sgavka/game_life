"""
First world UI logic.
todo: use animation on canvas
todo: draw statistic (make helpers for that)
"""

import tkinter as tk
import random
from typing import Tuple
from ui.helpers import ToolTip
from game.first_world import FirstWorld as WorldLogic, Unit, FoodObject, PoisonObject
from ui.main import World as WorldUI


class ParameterIncorrectException(Exception):
    """
    Exception for incorrect parameter.
    """
    pass


class FirstWorld(WorldUI):
    """
    First World UI class.
    """

    def __init__(self):
        super().__init__()

        self.set_cell_size_count_label = None
        self.cell_size_var = None
        self.cell_size_entry = None
        self.set_units_count_label = None
        self.units_count_var = None
        self.units_count_entry = None
        self.set_food_count_label = None
        self.food_count_var = None
        self.food_count_entry = None
        self.set_poison_count_label = None
        self.poison_count_var = None
        self.poison_count_entry = None
        self.count_x = None
        self.count_y = None
        self.cell_step = None
        self.cell_width = None
        self.width = None
        self.height = None
        self.game_canvas = None
        self.world = None
        self.game_frame = None

    def setup_cycles(self, frame: tk.Widget):
        """
        Setup GUI elements for Cycles.
        Need implementation.
        :param frame:
        """
        pass

    def setup_options(self, frame: tk.Widget):
        """

        :param frame:
        """
        # cell size
        self.set_cell_size_count_label = tk.Label(frame, text="Cell size:")
        self.set_cell_size_count_label.grid(row=0, column=0)
        ToolTip(self.set_cell_size_count_label, "Set size of cells in pixels.")

        self.cell_size_var = tk.StringVar()
        self.cell_size_var.set(9)
        self.cell_size_var.trace('w', self.change_cell_size_entry)

        self.cell_size_entry = tk.Entry(frame, textvariable=self.cell_size_var, width=5)
        self.cell_size_entry.grid(row=0, column=1)

        # units count
        self.set_units_count_label = tk.Label(frame, text="Count of Units:")
        self.set_units_count_label.grid(row=1, column=0)

        self.units_count_var = tk.StringVar()
        self.units_count_var.set(9)  # todo: move to options UI
        self.units_count_var.trace('w', self.change_units_count_entry)

        self.units_count_entry = tk.Entry(frame, textvariable=self.units_count_var, width=5)
        self.units_count_entry.grid(row=1, column=1)
        # todo: move to options UI
        # food count
        self.set_food_count_label = tk.Label(frame, text="Count of food:")
        self.set_food_count_label.grid(row=2, column=0)

        self.food_count_var = tk.StringVar()
        self.food_count_var.set(9)  # todo: move to options UI
        self.food_count_var.trace('w', self.change_food_count_entry)

        self.food_count_entry = tk.Entry(frame, textvariable=self.food_count_var, width=5)
        self.food_count_entry.grid(row=2, column=1)

        # poison count
        self.set_poison_count_label = tk.Label(frame, text="Count of poison:")
        self.set_poison_count_label.grid(row=3, column=0)

        self.poison_count_var = tk.StringVar()
        self.poison_count_var.set(9)  # todo: move to options UI
        self.poison_count_var.trace('w', self.change_poison_count_entry)

        self.poison_count_entry = tk.Entry(frame, textvariable=self.poison_count_var, width=5)
        self.poison_count_entry.grid(row=3, column=1)

    def setup_statistics(self, frame: tk.Widget):
        """
        Setup GUI elements for Statistics.
        Need implementation.
        :param frame:
        """
        pass

    def change_poison_count_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_food_count_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_units_count_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_cell_size_entry(self, *args):
        """

        :param args:
        """
        pass

    def setup(self, frame: tk.Widget, wight, height):
        """

        :param frame:
        :param wight:
        :param height:
        """
        # can set count of cells or set w&h in pixels
        # settings:
        self.count_x = wight
        self.count_y = height
        self.cell_step = int(self.cell_size_var.get())
        self.cell_width = 1
        self.width = self.count_x * (self.cell_step + self.cell_width)
        self.height = self.count_y * (self.cell_step + self.cell_width)

        self.game_frame = frame
        self.draw_canvas()
        self.world = WorldLogic(self.count_x, self.count_y)

    def draw_canvas(self):
        """
        Draw game canvas.
        """
        self.game_canvas = tk.Canvas(self.game_frame,
                                     width=int(self.width / (
                                         self.cell_step + self.cell_width)) * self.cell_step + self.cell_width,
                                     height=int(self.height / (
                                         self.cell_step + self.cell_width)) * self.cell_step + self.cell_width,
                                     bg='white')
        self.game_canvas.grid(row=0, column=0)

    def generate_random_unit(self, x, y):
        """

        :param x:
        :param y:
        """
        unit = Unit(self.world, x, y, Unit.GENOME_LEN * 3)
        unit.generate_random_genome()
        unit.set_body_direction(random.randrange(Unit.DIRECTION_NW))
        self.world.set_cell(x, y, unit)

    def setup_generation(self, generation):
        """
        Initial setup generation.
        """
        count_of_units_in_game = int(self.units_count_var.get())

        # generate rand units
        units_xy = [(random.randrange(0, self.world.width - 1), random.randrange(0, self.world.height - 1)) for _ in
                    range(count_of_units_in_game)]
        last_generation_units = self.world.get_units()
        if generation == 0 or len(last_generation_units) == 0:
            for (x, y) in units_xy:
                self.generate_random_unit(x, y)
        else:
            for (x, y, unit) in last_generation_units:
                self.world.set_cell(x, y, None)
            last_generation_units.sort(key=lambda tmp: tmp[2].get_body_energy(), reverse=True)
            parents_count = 2  # todo move to options UI
            parents = last_generation_units[:parents_count]
            parent: Tuple[int, int, Unit]
            i = 0
            generated_parents = int(count_of_units_in_game / parents_count) * parents_count
            for (_, _, unit) in parents:
                for _ in range(int(10 / parents_count)):
                    if i >= count_of_units_in_game:
                        break
                    x = units_xy[i][0]
                    y = units_xy[i][1]
                    unit_new = Unit(self.world, x, y, Unit.GENOME_LEN * 3)
                    unit_new.set_genome(unit.genome)
                    unit_new.mutate_genome(2, 10)  # todo: move to option UI
                    self.world.set_cell(x, y, unit_new)
                    i += 1
            i = 0
            for (x, y) in units_xy:
                self.generate_random_unit(x, y)
                i += 1
                if i >= generated_parents:
                    break

        # generate food
        food_xy = [(random.randrange(0, self.world.width), random.randrange(0, self.world.height)) for _ in
                   range(30)]  # todo: move to option UI
        for (x, y) in food_xy:
            food = FoodObject(random.randrange(100), x, y)  # todo: move to option UI
            self.world.set_cell(x, y, food)

        # generate poison
        poison_xy = [(random.randrange(0, self.world.width), random.randrange(0, self.world.height)) for _ in
                     range(30)]  # todo: move to option UI
        for (x, y) in poison_xy:
            poison = PoisonObject(random.randrange(-25, -1), x, y)  # todo: move to option UI
            self.world.set_cell(x, y, poison)

    def do_step(self):
        """
        Method implement step action.
        """
        # self.create_game_plot()

        self.world.do_step()

    def end_step(self, visualisation):
        """
        Actions after step execution.
        :param visualisation: bool
        """
        if visualisation:
            self.draw_canvas()
            for (_, _, food) in self.world.get_foods():
                self.draw_cell(food)
            for (_, _, poison) in self.world.get_poisons():
                self.draw_cell(poison)
            for (_, _, unit) in self.world.get_units():
                self.draw_cell(unit)

    def end_generation(self, visualisation):
        """

        :param visualisation: bool
        """
        if visualisation:
            pass

    def disable_options(self):
        """
        Disable additional options.
        """
        self.cell_size_entry['state'] = 'disabled'
        self.units_count_entry['state'] = 'disabled'
        self.food_count_entry['state'] = 'disabled'
        self.poison_count_entry['state'] = 'disabled'

    def draw_cell(self, cell):
        """

        :param cell:
        """
        x = cell.x
        y = cell.y
        color = 'white'
        if isinstance(cell, Unit):
            color = 'grey'
        elif isinstance(cell, FoodObject):
            color = 'green'
        elif isinstance(cell, PoisonObject):
            color = 'red'

        max_cell_x = int(self.width / (self.cell_step + self.cell_width))
        max_cell_y = int(self.height / (self.cell_step + self.cell_width))
        if 0 <= x < max_cell_x and 0 <= y < max_cell_y:
            start_x = 1 + self.cell_width + x * self.cell_step
            start_y = 1 + self.cell_width + y * self.cell_step
            end_x = self.cell_step + self.cell_width + x * self.cell_step
            end_y = self.cell_step + self.cell_width + y * self.cell_step
            self.game_canvas.create_rectangle(
                start_x,
                start_y,
                end_x,
                end_y,
                fill=color,
                outline="black"
            )
            if isinstance(cell, Unit):
                new_start_x = start_x + int((end_x - start_x) / 2)
                new_start_y = start_y + int((end_y - start_y) / 2)
                new_end_x, new_end_y = self.calculate_unit_direction_x_y(cell, start_x, start_y, end_x, end_y)
                self.game_canvas.create_line(
                    new_start_x,
                    new_start_y,
                    new_end_x,
                    new_end_y,
                    width=2
                )
        else:
            raise ParameterIncorrectException("max x = %s, max y = %s" % (max_cell_x - 1, max_cell_y - 1))

    @staticmethod
    def calculate_unit_direction_x_y(unit, start_x, start_y, end_x, end_y):
        """

        :param unit:
        :param start_x:
        :param start_y:
        :param end_x:
        :param end_y:
        :return:
        """
        half_x = start_x + int((end_x - start_x) / 2)
        half_y = start_y + int((end_y - start_y) / 2)
        new_x = 0
        new_y = 0
        direction = unit.get_body_direction()
        if direction == Unit.DIRECTION_N:
            new_x = half_x
            new_y = start_y
        elif direction == Unit.DIRECTION_NE:
            new_x = end_x
            new_y = start_y
        elif direction == Unit.DIRECTION_E:
            new_x = end_x
            new_y = half_y
        elif direction == Unit.DIRECTION_SE:
            new_x = end_x
            new_y = end_y
        elif direction == Unit.DIRECTION_S:
            new_x = half_x
            new_y = end_y
        elif direction == Unit.DIRECTION_WS:
            new_x = start_x
            new_y = end_y
        elif direction == Unit.DIRECTION_W:
            new_x = start_x
            new_y = half_y
        elif direction == Unit.DIRECTION_NW:
            new_x = start_x
            new_y = start_y
        return new_x, new_y

    def draw_grid(self):
        """
        Draw canvas grid.
        """
        # for x in range(self.cell_width, self.width, self.cell_step):
        #     self.game_canvas.create_line(x, 0, x, self.height, width=self.cell_width)
        self.game_canvas.create_line(self.width, 0, self.width, self.height, width=self.cell_width)
        # for y in range(self.cell_width, self.height, self.cell_step):
        #     self.game_canvas.create_line(0, y, self.width, y, width=self.cell_width)
        self.game_canvas.create_line(self.cell_width, self.height, self.width + self.cell_width, self.height,
                                     width=self.cell_width)
