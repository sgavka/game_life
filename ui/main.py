"""
File with main classes for GUI implementation and flow control of worlds.
"""

import tkinter as tk


class World:
    """
    Main class for GUI and flow logic of world.
    """

    def __init__(self):
        self.world = None

    def setup_cycles(self, frame: tk.Widget):
        """
        Setup GUI elements for Cycles.
        Need implementation.
        :param frame:
        """
        raise Exception()

    def setup_options(self, frame: tk.Widget):
        """
        Setup GUI elements for Options.
        Need implementation.
        :param frame:
        """
        raise Exception()

    def setup_statistics(self, frame: tk.Widget):
        """
        Setup GUI elements for Statistics.
        Need implementation.
        :param frame:
        """
        raise Exception()

    def setup(self, frame: tk.Widget, wight, height):
        """
        Initial setup of GUI World
        Need implementation.
        :param frame:
        :param wight:
        :param height:
        """
        raise Exception()

    def setup_generation(self, generation):
        """
        Initial setup generation.
        Need implementation.
        :type generation: int
        """
        raise Exception()

    def do_step(self):
        """
        Method implement step action.
        Need implementation.
        """
        raise Exception()

    def end_step(self, visualisation):
        """
        Actions after step execution.
        Need implementation.
        :param visualisation: bool
        """
        raise Exception()

    def end_generation(self, visualisation):
        """
        Action after generation execution (is called after all generation's steps).
        Need implementation.
        :param visualisation: bool
        """
        raise Exception()

    def disable_options(self):
        """
        Disable additional options.
        Need implementation.
        """
        raise Exception()
