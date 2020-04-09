"""
First world UI logic.
todo: use animation on canvas
todo: draw statistic (make helpers for that)
"""
import os
import sys
import tkinter as tk
import random
from typing import Tuple
import pygame as pg
from ui.helpers import ToolTip
from game.first_world import FirstWorld as WorldLogic, Unit, FoodObject, PoisonObject
from ui.main import World as WorldUI


class ParameterIncorrectException(Exception):
    """
    Exception for incorrect parameter.
    """
    pass


class FoodUI(pg.sprite.Sprite):
    """
    Food UI.
    """
    image: pg.Surface
    IMAGE = pg.image.load('ui/first_world_images/food.png')
    """
    Unit UI.
    """

    def __init__(self, group, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = self.IMAGE
        self.rect = self.image.get_rect(topleft=(x, y))
        self.add(group)

    def update(self):
        pass


class PoisonUI(FoodUI):
    """
    Poison UI.
    """
    IMAGE = pg.image.load('ui/first_world_images/poison.png')


class UnitUI(pg.sprite.Sprite):
    """
    Unit UI.
    """
    image: pg.Surface
    IMAGE_E = pg.image.load('ui/first_world_images/unit_E.png')
    IMAGE_N = pg.image.load('ui/first_world_images/unit_N.png')
    IMAGE_NE = pg.image.load('ui/first_world_images/unit_NE.png')
    IMAGE_NW = pg.image.load('ui/first_world_images/unit_NW.png')
    IMAGE_S = pg.image.load('ui/first_world_images/unit_S.png')
    IMAGE_SE = pg.image.load('ui/first_world_images/unit_SE.png')
    IMAGE_WS = pg.image.load('ui/first_world_images/unit_WS.png')
    IMAGE_W = pg.image.load('ui/first_world_images/unit_W.png')

    DIRECTION_TO_IMAGE = {
        Unit.DIRECTION_E: IMAGE_E,
        Unit.DIRECTION_N: IMAGE_N,
        Unit.DIRECTION_NE: IMAGE_NE,
        Unit.DIRECTION_NW: IMAGE_NW,
        Unit.DIRECTION_S: IMAGE_S,
        Unit.DIRECTION_SE: IMAGE_SE,
        Unit.DIRECTION_WS: IMAGE_WS,
        Unit.DIRECTION_W: IMAGE_W,
    }

    """
    Unit UI.
    """

    def __init__(self, direction, group, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = self.DIRECTION_TO_IMAGE[direction]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.add(group)

    def update(self):
        pass


class FirstWorld(WorldUI):
    """
    First World UI class.
    """
    world: WorldLogic

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
        self.game_screen = None
        self.parents_count_label = None
        self.parents_count_var = None
        self.parents_count_entry = None

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
        self.units_count_var.set(9)
        self.units_count_var.trace('w', self.change_units_count_entry)

        self.units_count_entry = tk.Entry(frame, textvariable=self.units_count_var, width=5)
        self.units_count_entry.grid(row=1, column=1)

        # food count
        self.set_food_count_label = tk.Label(frame, text="Count of food:")
        self.set_food_count_label.grid(row=2, column=0)

        self.food_count_var = tk.StringVar()
        self.food_count_var.set(9)
        self.food_count_var.trace('w', self.change_food_count_entry)

        self.food_count_entry = tk.Entry(frame, textvariable=self.food_count_var, width=5)
        self.food_count_entry.grid(row=2, column=1)

        # poison count
        self.set_poison_count_label = tk.Label(frame, text="Count of poison:")
        self.set_poison_count_label.grid(row=3, column=0)

        self.poison_count_var = tk.StringVar()
        self.poison_count_var.set(9)
        self.poison_count_var.trace('w', self.change_poison_count_entry)

        self.poison_count_entry = tk.Entry(frame, textvariable=self.poison_count_var, width=5)
        self.poison_count_entry.grid(row=3, column=1)

        # parents count
        self.parents_count_label = tk.Label(frame, text="Count of parents:")
        self.parents_count_label.grid(row=4, column=0)

        self.parents_count_var = tk.StringVar()
        self.parents_count_var.set(9)
        self.parents_count_var.trace('w', self.change_parents_count_entry)

        self.parents_count_entry = tk.Entry(frame, textvariable=self.parents_count_var, width=5)
        self.parents_count_entry.grid(row=4, column=1)

        # initial unit energy
        self.initial_unit_energy_label = tk.Label(frame, text="Initial unit energy:")
        self.initial_unit_energy_label.grid(row=5, column=0)

        self.initial_unit_energy_var = tk.StringVar()
        self.initial_unit_energy_var.set(100)
        self.initial_unit_energy_var.trace('w', self.change_initial_unit_energy_entry)

        self.initial_unit_energy_entry = tk.Entry(frame, textvariable=self.initial_unit_energy_var, width=5)
        self.initial_unit_energy_entry.grid(row=5, column=1)

        # genome mutate from
        self.genome_mutate_from_label = tk.Label(frame, text="Genome mutate from:")
        self.genome_mutate_from_label.grid(row=6, column=0)

        self.genome_mutate_from_var = tk.StringVar()
        self.genome_mutate_from_var.set(2)
        self.genome_mutate_from_var.trace('w', self.change_genome_mutate_from_entry)

        self.genome_mutate_from_entry = tk.Entry(frame, textvariable=self.genome_mutate_from_var, width=5)
        self.genome_mutate_from_entry.grid(row=6, column=1)

        # genome mutate to
        self.genome_mutate_to_label = tk.Label(frame, text="Genome mutate to:")
        self.genome_mutate_to_label.grid(row=7, column=0)

        self.genome_mutate_to_var = tk.StringVar()
        self.genome_mutate_to_var.set(10)
        self.genome_mutate_to_var.trace('w', self.change_genome_mutate_to_entry)

        self.genome_mutate_to_entry = tk.Entry(frame, textvariable=self.genome_mutate_to_var, width=5)
        self.genome_mutate_to_entry.grid(row=7, column=1)

        # food energy from
        self.food_energy_from_label = tk.Label(frame, text="Food energy from:")
        self.food_energy_from_label.grid(row=8, column=0)

        self.food_energy_from_var = tk.StringVar()
        self.food_energy_from_var.set(25)
        self.food_energy_from_var.trace('w', self.change_food_energy_from_entry)

        self.food_energy_from_entry = tk.Entry(frame, textvariable=self.food_energy_from_var, width=5)
        self.food_energy_from_entry.grid(row=8, column=1)

        # food energy to
        self.food_energy_to_label = tk.Label(frame, text="Food energy to:")
        self.food_energy_to_label.grid(row=9, column=0)

        self.food_energy_to_var = tk.StringVar()
        self.food_energy_to_var.set(50)
        self.food_energy_to_var.trace('w', self.change_food_energy_to_entry)

        self.food_energy_to_entry = tk.Entry(frame, textvariable=self.food_energy_to_var, width=5)
        self.food_energy_to_entry.grid(row=9, column=1)

        # poison energy from
        self.poison_energy_from_label = tk.Label(frame, text="Poison energy from:")
        self.poison_energy_from_label.grid(row=10, column=0)

        self.poison_energy_from_var = tk.StringVar()
        self.poison_energy_from_var.set(-50)
        self.poison_energy_from_var.trace('w', self.change_poison_energy_from_entry)

        self.poison_energy_from_entry = tk.Entry(frame, textvariable=self.poison_energy_from_var, width=5)
        self.poison_energy_from_entry.grid(row=10, column=1)

        # poison energy to
        self.poison_energy_to_label = tk.Label(frame, text="Poison energy to:")
        self.poison_energy_to_label.grid(row=11, column=0)

        self.poison_energy_to_var = tk.StringVar()
        self.poison_energy_to_var.set(-1)
        self.poison_energy_to_var.trace('w', self.change_poison_energy_to_entry)

        self.poison_energy_to_entry = tk.Entry(frame, textvariable=self.poison_energy_to_var, width=5)
        self.poison_energy_to_entry.grid(row=11, column=1)

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

    def change_parents_count_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_initial_unit_energy_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_genome_mutate_from_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_genome_mutate_to_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_food_energy_from_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_food_energy_to_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_poison_energy_from_entry(self, *args):
        """

        :param args:
        """
        pass

    def change_poison_energy_to_entry(self, *args):
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
        self.game_frame['width'] = self.width
        self.game_frame['height'] = self.height

        os.environ['SDL_WINDOWID'] = str(self.game_frame.winfo_id())
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        pg.display.init()

        # init pygame
        width = int(self.width / (self.cell_step + self.cell_width)) * self.cell_step + self.cell_width
        height = int(self.height / (self.cell_step + self.cell_width)) * self.cell_step + self.cell_width

        self.game_screen = pg.display.set_mode((width, height))

        self.draw_canvas()
        pg.display.flip()

        # init world logic
        self.world = WorldLogic(self.count_x, self.count_y)

    def draw_canvas(self):
        """
        Draw game canvas.
        """
        # fill game background
        self.game_screen.fill(pg.Color(255, 255, 255))

    def setup_generation(self, generation):
        """
        Initial setup generation.
        """
        self.world.set_generation_params(
            count_of_units_in_game=int(self.units_count_var.get()),
            parents_count=int(self.parents_count_entry.get()),
            initial_unit_energy=int(self.initial_unit_energy_var.get()),
            genome_mutate_from=int(self.genome_mutate_from_var.get()),
            genome_mutate_to=int(self.genome_mutate_to_var.get()),
            food_count=int(self.food_count_var.get()),
            food_energy_from=int(self.food_energy_from_var.get()),
            food_energy_to=int(self.food_energy_to_var.get()),
            poison_count=int(self.poison_count_var.get()),
            poison_energy_from=int(self.poison_energy_from_var.get()),
            poison_energy_to=int(self.poison_energy_to_var.get())
        )
        self.world.start_generation(generation)

    def do_step(self):
        """
        Method implement step action.
        """
        self.world.do_step()
        if len(self.world.get_units()):
            return False
        return True

    def end_step(self, visualisation):
        """
        Actions after step execution.
        :param visualisation: bool
        """
        if visualisation:
            self.draw_canvas()
            units = pg.sprite.Group()
            for (_, _, food) in self.world.get_foods():
                self.draw_cell(food, units)
            for (_, _, poison) in self.world.get_poisons():
                self.draw_cell(poison, units)
            for (_, _, unit) in self.world.get_units():
                self.draw_cell(unit, units)
            units.draw(self.game_screen)
            units.update()
            pg.display.flip()
            pg.time.delay(10)

    def end_generation(self, visualisation):
        """

        :param visualisation: bool
        """
        if visualisation:
            pass
        self.world.end_generation()

    def disable_options(self):
        """
        Disable additional options.
        """
        self.cell_size_entry['state'] = 'disabled'
        self.units_count_entry['state'] = 'disabled'
        self.food_count_entry['state'] = 'disabled'
        self.poison_count_entry['state'] = 'disabled'
        self.parents_count_entry['state'] = 'disabled'
        self.initial_unit_energy_entry['state'] = 'disabled'
        self.genome_mutate_from_entry['state'] = 'disabled'
        self.genome_mutate_to_entry['state'] = 'disabled'
        self.food_energy_from_entry['state'] = 'disabled'
        self.food_energy_to_entry['state'] = 'disabled'
        self.poison_energy_from_entry['state'] = 'disabled'
        self.poison_energy_to_entry['state'] = 'disabled'

    def enable_options(self):
        """
        Enable additional options.
        """
        self.cell_size_entry['state'] = 'normal'
        self.units_count_entry['state'] = 'normal'
        self.food_count_entry['state'] = 'normal'
        self.poison_count_entry['state'] = 'normal'
        self.parents_count_entry['state'] = 'normal'
        self.initial_unit_energy_entry['state'] = 'normal'
        self.genome_mutate_from_entry['state'] = 'normal'
        self.genome_mutate_to_entry['state'] = 'normal'
        self.food_energy_from_entry['state'] = 'normal'
        self.food_energy_to_entry['state'] = 'normal'
        self.poison_energy_from_entry['state'] = 'normal'
        self.poison_energy_to_entry['state'] = 'normal'

    def draw_cell(self, cell, units):
        """

        :param cell:
        """
        x = cell.x
        y = cell.y

        max_cell_x = int(self.width / (self.cell_step + self.cell_width))
        max_cell_y = int(self.height / (self.cell_step + self.cell_width))
        if 0 <= x < max_cell_x and 0 <= y < max_cell_y:
            start_x = 1 + self.cell_width + x * self.cell_step
            start_y = 1 + self.cell_width + y * self.cell_step

            if isinstance(cell, Unit):
                UnitUI(cell.get_body_direction(), units, start_x, start_y)
            elif isinstance(cell, FoodObject):
                FoodUI(units, start_x, start_y)
            elif isinstance(cell, PoisonObject):
                PoisonUI(units, start_x, start_y)
        else:
            raise ParameterIncorrectException("max x = %s, max y = %s" % (max_cell_x - 1, max_cell_y - 1))
