"""
First world logic classes.

todo: create unit tests
"""
import random

from game.main import World, Unit as MainUnit


class WorldObject:
    """
    Class for non Unit world objects.
    """
    def __init__(self, energy_change, x, y):
        self.energy_change = energy_change
        self.x = x
        self.y = y

    def do_on_step(self, unit: 'Unit'):
        """

        :param unit:
        """
        unit.change_energy(self.energy_change)


class FoodObject(WorldObject):
    """
    Class for Food.
    """
    pass


class PoisonObject(WorldObject):
    """
    Class for Poison.
    """
    pass


class EmptyObject(WorldObject):
    """
    Class for empty cells.
    """
    pass


class WallObject(WorldObject):
    """
    Class for Wall.
    """
    pass


class FirstWorld(World):
    """
    Class with world's logic.
    """
    def get_units(self):
        """

        :return:
        """
        return [
            (key_x, key_y, unit) for
            key_x, x in enumerate(self.cells) for
            key_y, unit in enumerate(x) if
            isinstance(unit, MainUnit)
        ]

    def get_foods(self):
        """

        :return:
        """
        return [
            (key_x, key_y, food) for
            key_x, x in enumerate(self.cells) for
            key_y, food in enumerate(x) if
            isinstance(food, FoodObject)
        ]

    def get_poisons(self):
        """

        :return:
        """
        return [
            (key_x, key_y, poison) for
            key_x, x in enumerate(self.cells) for
            key_y, poison in enumerate(x) if
            isinstance(poison, PoisonObject)
        ]

    def get_cell(self, x, y) -> 'WorldObject':
        """

        :param x:
        :param y:
        :return:
        """
        if 0 <= x < self.width and 0 <= y < self.height:  # todo: check if width and height is inclusive
            cell = self.cells[x][y]
            if cell is None:
                return EmptyObject(0, x, y)
            return cell
        else:
            return WorldObject(0, x, y)

    def do_step(self):
        """
        Start step logic of World.
        """
        unit: Unit
        for (x, y, unit) in self.get_units():
            unit.do_step()
            self.set_cell(x, y, None)
            if unit.is_alive():
                self.set_cell(unit.x, unit.y, unit)


class Unit(MainUnit):
    """
    Class with Unit logic.
    """

    GENOME_MOVE = 0
    GENOME_TURN = 1
    GENOME_EAT = 2
    GENOME_KILL = 3
    GENOME_LOOK = 4
    GENOME_CHECK_ENERGY = 5
    GENOME_GO_TO = 6  # and bigger

    GENOME_COMMANDS = {
        GENOME_MOVE: 'genome_command_move',
        GENOME_TURN: 'genome_command_turn',
        GENOME_EAT: 'genome_command_eat',
        GENOME_KILL: 'genome_command_kill',
        GENOME_LOOK: 'genome_command_look',
        GENOME_CHECK_ENERGY: 'genome_command_check_energy',
        GENOME_GO_TO: 'genome_command_go_to',
    }

    BODY_ENERGY = 0
    BODY_DIRECTION = 1  # 0 - N, 1 - NE, 2 - E, 3 - SE, 4 - S, 5 - WS, 6 - W, 7 - NW

    DIRECTION_N = 0
    DIRECTION_NE = 1
    DIRECTION_E = 2
    DIRECTION_SE = 3
    DIRECTION_S = 4
    DIRECTION_WS = 5
    DIRECTION_W = 6
    DIRECTION_NW = 7

    TURN_DIRECTION_LEFT = 0
    TURN_DIRECTION_RIGHT = 1

    BODY_PARAMS = {
        BODY_ENERGY: 0,
        BODY_DIRECTION: 1,
    }

    COST_OF_ENERGY_FOR_MOVE_ONE_STEP = -2
    COST_OF_ENERGY_FOR_EAT = -1
    COST_OF_ENERGY_FOR_KILL = -5
    COST_OF_ENERGY_FOR_RECYCLE = -3
    COST_OF_ENERGY_FOR_CHANGE_DIRECTION = -1
    COST_OF_ENERGY_FOR_LOOK = -1
    CHANGE_OF_ENERGY_FOR_ACCIDENTAL_DAMAGE = -1
    COEFFICIENT_OF_ENERGY_FOR_KILL = 3
    COEFFICIENT_OF_DAMAGE_FOR_KILL = 2

    def __init__(self, world: World, x, y, body_energy=100):  # todo: move body energy to GUI settings
        super().__init__(world, x, y)

        self.body = {
            self.BODY_ENERGY: body_energy,
            self.BODY_DIRECTION: 0,
        }

        self.damage = self.CHANGE_OF_ENERGY_FOR_ACCIDENTAL_DAMAGE

    def mutate_genome(self, gen_diff_probability, probability: int):
        """

        :param gen_diff_probability:
        :param probability:
        """
        i = 0
        for gen_old in self.genome:
            if random.randrange(100) > probability:
                self.genome[i] = gen_old
            else:
                gen_diff = random.randrange(gen_diff_probability)
                mutation_sign = random.randrange(1)
                if mutation_sign == 0:
                    if gen_diff + gen_old < self.GENOME_LEN:
                        gen_new = gen_old + gen_diff
                    else:
                        gen_new = gen_old - gen_diff
                else:
                    if gen_old - gen_diff >= 0:
                        gen_new = gen_old - gen_diff
                    else:
                        gen_new = gen_old + gen_diff
                self.genome[i] = gen_new
            i += 1

    def do_step(self):
        """
        Start step logic of Unit.
        """
        command = self.get_actual_gen()
        if command > self.GENOME_GO_TO:
            command = self.GENOME_GO_TO
        getattr(self, self.GENOME_COMMANDS[command])()

        self.call_genome_command(command)

        self.change_energy(-1)  # energy for every step

    def get_body_direction(self):
        """

        :return:
        """
        return self.body[self.BODY_DIRECTION]

    def set_body_direction(self, direction):
        """

        :param direction:
        """
        # todo: add validation
        self.body[self.BODY_DIRECTION] = direction

    def genome_command_move(self):
        """
        Implementation of genome command Move.
        """
        direction = self.get_body_direction()
        # steps = self.get_next_genome_value()
        self.increase_genome_pointer()

        steps = 1  # do 1 step
        new_x, new_y = self.calculate_new_coordinate(direction, steps)
        new_cell = self.world.get_cell(new_x, new_y)
        self.calculate_and_move_to_cell(new_cell, new_x, new_y, steps)

    def calculate_and_move_to_cell(self, cell, x, y, steps):
        """

        :param cell:
        :param x:
        :param y:
        :param steps:
        """
        if isinstance(cell, EmptyObject):
            self.x = x
            self.y = y
        elif isinstance(cell, FoodObject) or isinstance(cell, PoisonObject):
            cell.do_on_step(self)
            self.world.set_cell(x, y, None)
            self.x = x
            self.y = y
        elif isinstance(cell, MainUnit) or isinstance(cell, WallObject):
            cell.do_on_step(self)
        self.change_energy(self.COST_OF_ENERGY_FOR_MOVE_ONE_STEP * steps)

    def calculate_new_coordinate(self, direction, steps):
        """

        :param direction:
        :param steps:
        :return:
        """
        new_x = self.x
        new_y = self.y
        if direction == self.DIRECTION_N:
            new_y -= steps
        elif direction == self.DIRECTION_NE:
            new_x += steps
            new_y -= steps
        elif direction == self.DIRECTION_E:
            new_x += steps
        elif direction == self.DIRECTION_SE:
            new_x += steps
            new_y += steps
        elif direction == self.DIRECTION_S:
            new_y += steps
        elif direction == self.DIRECTION_WS:
            new_x -= steps
            new_y += steps
        elif direction == self.DIRECTION_W:
            new_x -= steps
        elif direction == self.DIRECTION_NW:
            new_x -= steps
            new_y -= steps
        return new_x, new_y

    def genome_command_turn(self):
        """
        Implementation of genome command Turn.
        """
        direction = self.get_body_direction()
        turn_direction = self.get_next_genome_value()
        self.increase_genome_pointer()

        if turn_direction < int(self.GENOME_MAX_VALUE / 2):
            turn = self.TURN_DIRECTION_LEFT
        else:
            turn = self.TURN_DIRECTION_RIGHT

        new_direction = direction
        new_direction += turn
        if turn == self.TURN_DIRECTION_RIGHT:
            if new_direction > self.DIRECTION_NW:
                new_direction = new_direction - self.DIRECTION_NW - 1
        elif turn == self.TURN_DIRECTION_LEFT:
            if new_direction < self.DIRECTION_N:
                new_direction = self.DIRECTION_NW + new_direction + 1
        self.set_body_direction(new_direction)

    def genome_command_eat(self):
        """
        Implementation of genome command Eat.
        """
        direction = self.get_body_direction()
        new_x, new_y = self.calculate_new_coordinate(direction, 1)
        new_cell = self.world.get_cell(new_x, new_y)
        self.change_energy(self.COST_OF_ENERGY_FOR_EAT)
        self.calculate_and_move_to_cell(new_cell, new_x, new_y, 1)
        self.increase_genome_pointer()

    def genome_command_kill(self):
        """
        Implementation of genome command Kill.
        """
        direction = self.get_body_direction()
        self.damage = self.get_next_genome_value() * -1
        self.increase_genome_pointer()

        new_x, new_y = self.calculate_new_coordinate(direction, 1)
        new_cell = self.world.get_cell(new_x, new_y)

        self.calculate_and_move_to_cell(new_cell, new_x, new_y, 1)
        self.damage = self.CHANGE_OF_ENERGY_FOR_ACCIDENTAL_DAMAGE

    def genome_command_look(self):
        """
        Implementation of genome command Look.
        """
        self.change_energy(self.COST_OF_ENERGY_FOR_LOOK)

        direction = self.get_body_direction()
        genome_to_do_then_empty = self.get_next_genome_value()
        genome_to_do_then_wall = self.get_next_genome_value(2)
        genome_to_do_then_food = self.get_next_genome_value(3)
        genome_to_do_then_poison = self.get_next_genome_value(4)
        genome_to_do_then_unit = self.get_next_genome_value(5)

        new_x, new_y = self.calculate_new_coordinate(direction, 1)
        new_cell = self.world.get_cell(new_x, new_y)

        if isinstance(new_cell, EmptyObject):
            self.genome_point = genome_to_do_then_empty
        elif isinstance(new_cell, FoodObject):
            self.genome_point = genome_to_do_then_food
        elif isinstance(new_cell, PoisonObject):
            self.genome_point = genome_to_do_then_poison
        elif isinstance(new_cell, MainUnit):
            self.genome_point = genome_to_do_then_unit
        elif isinstance(new_cell, WallObject):
            self.genome_point = genome_to_do_then_wall
        self.increase_genome_pointer()

    def genome_command_check_energy(self):
        """
        Implementation of genome command Check Energy.
        """
        value = self.get_next_genome_value()
        genome_to_do_then_more = self.get_next_genome_value(2)
        genome_to_do_then_less = self.get_next_genome_value(3)
        genome_to_do_then_equal = self.get_next_genome_value(4)

        body_energy = self.body[self.BODY_ENERGY]
        if value > body_energy:
            self.genome_point = genome_to_do_then_more
        elif value < body_energy:
            self.genome_point = genome_to_do_then_less
        elif value == body_energy:
            self.genome_point = genome_to_do_then_equal
        self.increase_genome_pointer()

    def genome_command_go_to(self):
        """
        Implementation of genome command Go To.
        """
        genome_to_do = self.get_next_genome_value()
        self.genome_point = genome_to_do

    def change_energy(self, count):
        """
        Change body energy.
        :param count:
        """
        self.body[self.BODY_ENERGY] += count

    def get_body_energy(self):
        """

        :return:
        """
        return self.body[self.BODY_ENERGY]

    def do_on_step(self, unit: 'Unit'):
        """

        :param unit:
        """
        self.change_energy(unit.COST_OF_ENERGY_FOR_KILL * unit.damage)
        unit_energy = unit.body[self.BODY_ENERGY]
        unit.change_energy(unit.damage * unit.COEFFICIENT_OF_DAMAGE_FOR_KILL)
        if not unit.is_alive():
            self.x = unit.x
            self.y = unit.y
            self.change_energy(unit_energy * unit.COEFFICIENT_OF_ENERGY_FOR_KILL)

    def is_alive(self):
        """

        :return:
        """
        return self.body[self.BODY_ENERGY] > 0
