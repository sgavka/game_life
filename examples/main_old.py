# todo: check if directions is draw correct (or it is equal for all units)
# todo: create ability to hide plot
# todo: create visual editor and browser for genome
import time
import tkinter as tk
import random
from typing import Tuple

import numpy
import pylab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import Colormap, ListedColormap
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pandas import DataFrame

import game
from game import Unit


class ParameterIncorrectException(Exception):
    pass


class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master

        self.master.geometry('1200x926')
        self.master.title('Life Game')

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.create_widgets()

    def game_set_unit_genome_preset(self, unit):
        preset = 2
        if preset == 0:
            unit.genome[0] = game.Unit.GENOME_MOVE
            unit.genome[1] = game.Unit.GENOME_MOVE
            unit.genome[2] = game.Unit.GENOME_MOVE
            unit.genome[3] = game.Unit.GENOME_MOVE
        elif preset == 1:
            unit.genome[0] = game.Unit.GENOME_LOOK

            unit.genome[1] = game.Unit.GENOME_MOVE

            unit.genome[2] = game.Unit.GENOME_TURN
            unit.genome[3] = random.randrange(64)

            unit.genome[4] = game.Unit.GENOME_MOVE

            unit.genome[5] = game.Unit.GENOME_TURN
            unit.genome[6] = random.randrange(64)

            unit.genome[7] = game.Unit.GENOME_TURN
            unit.genome[8] = random.randrange(64)
        elif preset == 2:
            unit.genome[0] = game.Unit.GENOME_LOOK

            unit.genome[1] = game.Unit.GENOME_MOVE

            unit.genome[2] = game.Unit.GENOME_GO_TO
            unit.genome[3] = 9

            unit.genome[4] = game.Unit.GENOME_MOVE

            unit.genome[2] = game.Unit.GENOME_GO_TO
            unit.genome[3] = 9

            unit.genome[2] = game.Unit.GENOME_GO_TO
            unit.genome[3] = 9

            unit.genome[9] = game.Unit.GENOME_TURN
            unit.genome[10] = random.randrange(64)

            unit.genome[11] = game.Unit.GENOME_LOOK

            unit.genome[12] = game.Unit.GENOME_MOVE

            unit.genome[13] = game.Unit.GENOME_GO_TO
            unit.genome[14] = 20

            unit.genome[15] = game.Unit.GENOME_MOVE

            unit.genome[16] = game.Unit.GENOME_GO_TO
            unit.genome[17] = 20

            unit.genome[18] = game.Unit.GENOME_GO_TO
            unit.genome[19] = 20

            unit.genome[20] = game.Unit.GENOME_TURN
            unit.genome[21] = random.randrange(64)

            unit.genome[22] = 0

            unit.genome[23] = game.Unit.GENOME_TURN
            unit.genome[24] = random.randrange(64)
            unit.genome[25] = game.Unit.GENOME_TURN
            unit.genome[26] = unit.genome[24]

    def game_generate_random_unit(self, world, x, y):
        unit = game.Unit(world, x, y, game.Unit.GENOME_LEN * 3)
        unit.generate_random_genome()
        self.game_set_unit_genome_preset(unit)
        unit.set_body_direction(random.randrange(7))
        world.set_cell(x, y, unit)

    def start_game_command(self):
        generation = 0
        self.generation_lable = tk.Label(self.option_frame, text="Generation — " + str(generation))
        self.generation_lable.grid(row=1, column=0)
        self.step_lable = tk.Label(self.option_frame, text="Step — *game starts*")
        self.step_lable.grid(row=2, column=0)
        world = game.World()
        while True:
            count_of_units_in_game = 15
            generation_steps = game.Unit.GENOME_LEN * 3
            # generate rand units
            units_xy = [(random.randrange(0, world.width), random.randrange(0, world.height)) for i in range(count_of_units_in_game)]
            last_generation_units = world.get_units()
            if generation == 0 or len(last_generation_units) == 0:
                for (x, y) in units_xy:
                    self.game_generate_random_unit(world, x, y)
            else:
                for (x, y, unit) in last_generation_units:
                    world.set_cell(x, y, None)
                last_generation_units.sort(key=lambda x: x[2].get_body_energy(), reverse=True)
                parents_count = 2
                parents = last_generation_units[:parents_count]
                parent: Tuple[int, int, Unit]
                i = 0
                generated_parents = int(count_of_units_in_game / parents_count) * parents_count
                for (_, __, unit) in parents:
                    for _ in range(int(10 / parents_count)):
                        x = units_xy[i][0]
                        y = units_xy[i][1]
                        unit_new = Unit(world, x, y, game.Unit.GENOME_LEN * 3)
                        unit_new.set_genome(unit.genome)
                        unit_new.mutate_genome(2, 10)
                        world.set_cell(x, y, unit_new)
                        i += 1
                i = 0
                for (x, y) in units_xy:
                    self.game_generate_random_unit(world, x, y)
                    i += 1
                    if i >= generated_parents:
                        break
            # generate food
            food_xy = [(random.randrange(0, world.width), random.randrange(0, world.height)) for i in range(30)]
            for (x, y) in food_xy:
                food = game.FoodObject(random.randrange(100), x, y)
                world.set_cell(x, y, food)

            # generate poison
            poison_xy = [(random.randrange(0, world.width), random.randrange(0, world.height)) for i in range(30)]
            for (x, y) in poison_xy:
                poison = game.PoisonObject(random.randrange(-25, -1), x, y)
                world.set_cell(x, y, poison)

            step = 0
            while True:
                units = world.get_units()  # some unit can be replaced by food or poison
                if len(units) == 0:
                    break
                self.create_game_plot()

                foods = world.get_foods()
                for (x, y, food) in foods:
                    self.draw_cell(food)
                poisons = world.get_poisons()
                for (x, y, poison) in poisons:
                    self.draw_cell(poison)
                for (x, y, unit) in units:
                    self.draw_cell(unit)
                world.start(1)
                self.master.update()
                step += 1
                if step >= generation_steps:
                    break
                self.step_lable.config(text="Step — " + str(step))
                pass
            generation += 1
            self.generation_lable.config(text="Generation — " + str(generation))
            self.draw_cells_genome(world)
            pass
        pass

    def draw_cells_genome(self, world):
        # self.genomes_frame.pack_forget()
        # self.genomes_frame.update()

        # for widget in self.genomes_frame.winfo_children():
        #     widget.destroy()
        # self.genomes_frame.destroy()
        # self.genomes_frame.grid_forget()
        unit: game.Unit
        grid_i = 0
        for (x, y, unit) in world.get_units():
            frame = tk.LabelFrame(self.genomes_frame, text="Unit [" + str(x) + ", " + str(y) + "]")
            i = 0
            while i < game.Unit.GENOME_MAX_VALUE:
                genome = unit.genome[i]
                if genome == game.Unit.GENOME_TURN:
                    str_genome = 'T:'
                    str_genome += str(unit.genome[i + 1])
                    i += 1
                elif genome == game.Unit.GENOME_MOVE:
                    str_genome = 'M:'
                    str_genome += str(unit.genome[i + 1])
                    i += 1
                elif genome == game.Unit.GENOME_EAT:
                    str_genome = 'E'
                elif genome == game.Unit.GENOME_KILL:
                    str_genome = 'K:'
                    str_genome += str(unit.genome[i + 1])
                    i += 1
                elif genome == game.Unit.GENOME_LOOK:
                    str_genome = 'L'
                elif genome == game.Unit.GENOME_CHECK_ENERGY:
                    str_genome = 'C:'
                    str_genome += str(unit.genome[i + 1])
                    str_genome += "|" + str(unit.genome[i + 1])
                    str_genome += "|" + str(unit.genome[i + 1])
                    i += 3
                else:
                    str_genome = 'G:'
                    str_genome += str(unit.genome[i + 1])
                    i += 1
                button = tk.Button(frame, text=str_genome).pack()
                i += 1
            frame.grid(row=grid_i, column=0)
            self.master.update()
            grid_i += 1

    def create_widgets(self):
        self.game_frame = tk.LabelFrame(self.master, text="Game")
        self.game_frame.grid(row=0, column=0, rowspan=2)

        self.option_frame = tk.LabelFrame(self.master, text="Options")
        self.option_frame.grid(row=0, column=1)

        self.start_game = tk.Button(self.option_frame, text="Start Game!", command=self.start_game_command)
        self.start_game.grid(row=0, column=0)

        # self.scrollbar = tk.Scrollbar(self.master)
        # self.scrollbar.grid()  # side=tk.RIGHT, fill=tk.Y
        # self.master.yscrollcommand = self.scrollbar.set

        # scrollderoot = tk.Scrollbar(orient="vertical", command=self.master)
        # scrollderoot.grid(column=5, row=0, sticky='ns',
        #                   in_=root)  # instead of number 5, set the column as the expected one for the scrollbar. Sticky ns will might be neccesary.
        # self.master.configure(yscrollcommand=scrollderoot.set)

        self.genomes_frame = tk.LabelFrame(self.master, text="Genomes")
        self.genomes_frame.grid(row=1, column=1)

        self.create_game_plot()

    def create_game_plot(self):
        # can set count of cells or set w&h in pixels
        # settings:
        self.count_x = 100
        self.count_y = 100
        self.cell_step = 9
        self.cell_width = 1
        self.width = self.count_x * (self.cell_step + self.cell_width)
        self.height = self.count_y * (self.cell_step + self.cell_width)

        self.game_canvas = tk.Canvas(self.game_frame,
                                     width=int(self.width / (self.cell_step + self.cell_width)) * self.cell_step + self.cell_width,
                                     height=int(self.height / (self.cell_step + self.cell_width)) * self.cell_step + self.cell_width,
                                     bg='white')
        self.game_canvas.grid(row=0, column=0)

    def draw_cell(self, cell):
        x = cell.x
        y = cell.y
        color = 'white'
        if isinstance(cell, game.Unit):
            color = 'grey'
        elif isinstance(cell, game.FoodObject):
            color = 'green'
        elif isinstance(cell, game.PoisonObject):
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
            if isinstance(cell, game.Unit):
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

    def calculate_unit_direction_x_y(self, unit, start_x, start_y, end_x, end_y):
        half_x = start_x + int((end_x - start_x) / 2)
        half_y = start_y + int((end_y - start_y) / 2)
        new_x = 0
        new_y = 0
        direction = unit.get_body_direction()
        if direction == game.Unit.DIRECTION_N:
            new_x = half_x
            new_y = start_y
        elif direction == game.Unit.DIRECTION_NE:
            new_x = end_x
            new_y = start_y
        elif direction == game.Unit.DIRECTION_E:
            new_x = end_x
            new_y = half_y
        elif direction == game.Unit.DIRECTION_SE:
            new_x = end_x
            new_y = end_y
        elif direction == game.Unit.DIRECTION_S:
            new_x = half_x
            new_y = end_y
        elif direction == game.Unit.DIRECTION_WS:
            new_x = start_x
            new_y = end_y
        elif direction == game.Unit.DIRECTION_W:
            new_x = start_x
            new_y = half_y
        elif direction == game.Unit.DIRECTION_NW:
            new_x = start_x
            new_y = start_y
        return new_x, new_y

    def draw_grid(self):
        # for x in range(self.cell_width, self.width, self.cell_step):
        #     self.game_canvas.create_line(x, 0, x, self.height, width=self.cell_width)
        self.game_canvas.create_line(self.width, 0, self.width, self.height, width=self.cell_width)
        # for y in range(self.cell_width, self.height, self.cell_step):
        #     self.game_canvas.create_line(0, y, self.width, y, width=self.cell_width)
        self.game_canvas.create_line(self.cell_width, self.height, self.width + self.cell_width, self.height, width=self.cell_width)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
