"""
Main file of application.

todo: write to file functional (start/stop button)
todo: UI fixes
todo: create readme
todo: create docs
"""

import tkinter as tk
from tkinter import filedialog, StringVar
import os
from ui.first_world import FirstWorld
from ui.helpers import ToolTip
from ui.main import World


class Application(tk.Frame):
    """
    Applicatoin.
    """
    world_height_var: StringVar
    world_width_var: StringVar
    world_ui: World
    filename: str

    def __init__(self):
        self.game_is_started = False
        self.game_is_break = False
        self.step_count = 0
        self.generation_count = 0
        self.root = tk.Tk()
        super().__init__(self.root)

        self.is_visualisation_on = True

        self.world_options = []
        self.world_values = {}

        self.root.title('Life Game')

        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.pack(pady=5, padx=5)

        self.setup_game_frame = None
        self.start_button = None
        self.hide_visualisation_button = None
        self.cycles_frame = None
        self.player_frame = None
        self.statistics_frame = None
        self.game_frame = None
        self.options_frame = None
        self.open_file_label = None
        self.open_file_button = None
        self.select_world_label = None
        self.world_var = None
        self.worlds_dropdown = None
        self.set_generations_count_label = None
        self.generations_var = None
        self.generations_entry = None
        self.set_steps_count_label = None
        self.steps_var = None
        self.steps_entry = None
        self.set_world_width_count_label = None
        self.world_width_var = None
        self.world_width_entry = None
        self.set_world_height_count_label = None
        self.world_height_var = None
        self.world_height_entry = None
        self.additional_game_options_frame = None
        self.generation_label = None
        self.generation_count_label = None
        self.step_label = None
        self.step_count_label = None
        self.additional_cycles_frame = None
        self.player_pause = None
        self.player_pause_tooltip = None
        self.player_is_on_pause = False

    def init_widgets(self):
        """
        Init all widgets.
        """
        self.game_frame = tk.LabelFrame(self.main_frame, text="Game")
        self.game_frame.grid(row=0, column=0)

        self.options_frame = tk.LabelFrame(self.main_frame, text="Options")
        self.options_frame.grid(row=0, column=1, sticky=tk.S + tk.N + tk.W + tk.E)
        self.fill_options_frame()

    def add_world(self, world_name, world):
        """
        Add type of world to list.
        :param world_name: 
        :param world: 
        """
        self.world_options.append(world_name)
        self.world_values[world_name] = world

    def start(self):
        """
        Start application.
        """
        self.init_widgets()

        self.mainloop()

    def change_world_dropdown(self, *args):
        """
        Handler for dropdown then is chosen another World type.
        :param args: 
        """
        self.root.title(self.root.title() + ": " + self.world_var.get())

        self.world_ui = self.world_values[self.world_var.get()]()
        self.world_ui.setup_cycles(self.additional_cycles_frame)
        self.world_ui.setup_options(self.additional_game_options_frame)
        self.world_ui.setup_statistics(self.statistics_frame)

    def fill_options_frame(self):
        """
        Setup of Options frame.
        """
        # setup game frame
        self.setup_game_frame = tk.LabelFrame(self.options_frame, text="Setup game")
        self.setup_game_frame.grid(row=0, column=0)
        self.fill_setup_game_frame()

        # start button
        self.start_button = tk.Button(self.options_frame, text="Start Game!", command=self.start_command)
        self.start_button.grid(row=1, column=0, sticky=tk.W + tk.E, columnspan=2)

        # hide visualisation button
        self.hide_visualisation_button = tk.Button(self.options_frame, text="Hide visualisation",
                                                   command=self.hide_visualisation_command)
        self.hide_visualisation_button.grid(row=2, column=0, columnspan=2)

        # cycles frame
        self.cycles_frame = tk.LabelFrame(self.options_frame, text="Cycles")
        self.cycles_frame.grid(row=3, column=0, sticky=tk.W + tk.E, columnspan=2)
        self.fill_cycles_frame()

        # player frame
        self.player_frame = tk.LabelFrame(self.options_frame, text="Player")
        self.player_frame.grid(row=4, column=0, sticky=tk.W + tk.E, columnspan=2)
        self.fill_player_frame()

        # statistics frame
        self.statistics_frame = tk.LabelFrame(self.options_frame, text="Statistics")
        self.statistics_frame.grid(row=5, column=0, sticky=tk.W + tk.E, columnspan=2)

    def fill_setup_game_frame(self):
        """
        Setup Setup Game frame.
        """
        self.open_file_label = tk.Label(self.setup_game_frame, text="Load Game from file:")
        self.open_file_label.grid(row=0, column=0)
        self.open_file_button = tk.Button(self.setup_game_frame, text="Open", command=self.open_file_command)
        self.open_file_button.grid(row=0, column=1)

        tk.Label(self.setup_game_frame, text="or start new:").grid(row=1, column=0, columnspan=2)

        self.select_world_label = tk.Label(self.setup_game_frame, text="World:")
        self.select_world_label.grid(row=2, column=0)
        ToolTip(self.select_world_label, "Select world")
        self.world_var = tk.StringVar(self.setup_game_frame)
        self.world_var.set(self.world_options[0])
        self.world_ui = self.world_values[self.world_options[0]]()  # default world
        self.worlds_dropdown = tk.OptionMenu(self.setup_game_frame, self.world_var, *self.world_options)
        self.worlds_dropdown.grid(row=2, column=1)
        self.world_var.trace('w', self.change_world_dropdown)

        self.set_generations_count_label = tk.Label(self.setup_game_frame, text="Generations:")
        self.set_generations_count_label.grid(row=3, column=0)
        ToolTip(self.set_generations_count_label, "Set maximum count of generations. 0 for infinite.")
        self.generations_var = tk.StringVar()
        self.generations_var.set(0)
        self.generations_var.trace('w', self.change_generations_entry)
        self.generations_entry = tk.Entry(self.setup_game_frame, textvariable=self.generations_var, width=5)
        self.generations_entry.grid(row=3, column=1)

        self.set_steps_count_label = tk.Label(self.setup_game_frame, text="Steps:")
        self.set_steps_count_label.grid(row=4, column=0)
        ToolTip(self.set_steps_count_label, "Set maximum count of steps.")
        self.steps_var = tk.StringVar()
        self.steps_var.set(100)
        self.steps_var.trace('w', self.change_steps_entry)
        self.steps_entry = tk.Entry(self.setup_game_frame, textvariable=self.steps_var, width=5)
        self.steps_entry.grid(row=4, column=1)

        self.set_world_width_count_label = tk.Label(self.setup_game_frame, text="World width:")
        self.set_world_width_count_label.grid(row=5, column=0)
        ToolTip(self.set_world_width_count_label, "Set count of cells on X ax.")
        self.world_width_var = tk.StringVar()
        self.world_width_var.set(100)
        self.world_width_var.trace('w', self.change_world_width_entry)
        self.world_width_entry = tk.Entry(self.setup_game_frame, textvariable=self.world_width_var, width=5)
        self.world_width_entry.grid(row=5, column=1)

        self.set_world_height_count_label = tk.Label(self.setup_game_frame, text="World height:")
        self.set_world_height_count_label.grid(row=6, column=0)
        ToolTip(self.set_world_height_count_label, "Set count of cells on Y ax.")
        self.world_height_var = tk.StringVar()
        self.world_height_var.set(100)
        self.world_height_var.trace('w', self.change_world_height_entry)
        self.world_height_entry = tk.Entry(self.setup_game_frame, textvariable=self.world_height_var, width=5)
        self.world_height_entry.grid(row=6, column=1)

        # self.set_cell_size_count_label = tk.Label(self.setup_game_frame, text="Cell size:")
        # self.set_cell_size_count_label.grid(row=7, column=0)
        # ToolTip(self.set_cell_size_count_label, "Set size of cells in pixels.")
        # self.cell_size_var = tk.StringVar()
        # self.cell_size_var.set(9)
        # self.cell_size_var.trace('w', self.change_cell_size_entry)
        # self.cell_size_entry = tk.Entry(self.setup_game_frame, textvariable=self.cell_size_var, width=5)
        # self.cell_size_entry.grid(row=7, column=1)

        self.additional_game_options_frame = tk.LabelFrame(self.setup_game_frame, text="Additional game options")
        self.additional_game_options_frame.grid(row=7, column=0, sticky=(tk.N, tk.W, tk.E, tk.S), columnspan=2)
        self.change_world_dropdown()  # setup world UI on initialisation for default world

    def open_file_command(self):
        """
        Open the file with world presets.
        """
        self.filename = tk.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                                      filetypes=(("game files", "*.game"), ("all files", "*.*")))
        self.open_file_button['text'] = "Opened (" + self.filename.split(os.path.sep)[-1] + ")"
        self.worlds_dropdown['state'] = 'disabled'
        self.generations_entry['state'] = 'disabled'
        self.steps_entry['state'] = 'disabled'
        self.world_width_entry['state'] = 'disabled'
        self.world_height_entry['state'] = 'disabled'

    def change_cell_size_entry(self, *args):
        """

        :param args: 
        """
        pass  # self.cell_size_var.get()

    def change_world_height_entry(self, *args):
        """

        :param args: 
        """
        pass  # self.world_height_var.get()

    def change_world_width_entry(self, *args):
        """

        :param args: 
        """
        pass  # self.world_width_var.get()

    def change_generations_entry(self, *args):
        """

        :param args: 
        """
        pass  # self.generations_var.get()

    def change_steps_entry(self, *args):
        """

        :param args: 
        """
        pass  # self.steps_var.get()

    def fill_statistics_frame(self):
        """
        Fill statistics frame.
        """
        pass  # dynamical buttons with statistic

    def fill_cycles_frame(self):
        """
        Fill cycles frame.
        """
        self.generation_label = tk.Label(self.cycles_frame, text="Generation:")
        self.generation_label.grid(row=0, column=0)

        self.generation_count_label = tk.Label(self.cycles_frame, text="0")
        self.generation_count_label.grid(row=0, column=1)

        self.step_label = tk.Label(self.cycles_frame, text="Step:")
        self.step_label.grid(row=1, column=0)

        self.step_count_label = tk.Label(self.cycles_frame, text="0")
        self.step_count_label.grid(row=1, column=1)

        # frame to dynamically add info about cycles (packed frames)
        self.additional_cycles_frame = tk.LabelFrame(self.options_frame, text="Additional cycles")
        self.additional_cycles_frame.grid(row=2, column=0, columnspan=2)

    def fill_player_frame(self):
        """
        Fill player frame.
        """
        self.player_pause = tk.Button(self.player_frame, text="||", state='disabled', command=self.player_pause_command)
        self.player_pause.grid(row=0, column=0)
        self.player_pause_tooltip = ToolTip(self.player_pause, "Pause")

    def hide_visualisation_command(self):
        """
        Hide visualisation button command.
        """
        if self.is_visualisation_on:
            self.hide_visualisation_button['text'] = "Hide visualisation"
            self.is_visualisation_on = False
        else:
            self.hide_visualisation_button['text'] = "Show visualisation"
            self.is_visualisation_on = True

    def start_command(self, unpause=False):
        """
        Start button command.
        """
        self.open_file_button['state'] = 'disabled'
        self.worlds_dropdown['state'] = 'disabled'
        self.generations_entry['state'] = 'disabled'
        self.steps_entry['state'] = 'disabled'
        self.world_height_entry['state'] = 'disabled'
        self.world_width_entry['state'] = 'disabled'
        self.world_ui.disable_options()

        self.player_pause['state'] = 'normal'

        if not unpause and self.game_is_started:
            self.game_is_started = False
            self.generation_count_label['text'] = '0'
            self.step_count_label['text'] = '0'
            self.start_button['text'] = "Start Game!"
            self.player_pause['text'] = '||'
            self.player_pause_tooltip.text = "Pause"

            self.open_file_button['state'] = 'normal'
            self.worlds_dropdown['state'] = 'normal'
            self.generations_entry['state'] = 'normal'
            self.steps_entry['state'] = 'normal'
            self.world_height_entry['state'] = 'normal'
            self.world_width_entry['state'] = 'normal'
            self.world_ui.enable_options()

            self.player_is_on_pause = False
            return
        self.start_button['text'] = "End Game!"
        self.game_is_started = True
        if not unpause:
            self.generation_count = 0
            self.world_ui.setup(self.game_frame, int(self.world_width_var.get()), int(self.world_height_var.get()))
            self.game_is_break = False
        while True:
            if not self.game_is_break:
                self.world_ui.setup_generation(self.generation_count)
                self.step_count = 0
            else:
                self.game_is_break = False
            while True:
                if not self.game_is_started:
                    break
                if self.player_is_on_pause:
                    self.game_is_break = True
                    break
                end_generation = self.world_ui.do_step()
                self.step_count += 1
                if self.step_count >= int(self.steps_var.get()) or end_generation:
                    break
                self.step_count_label['text'] = str(self.step_count)
                self.world_ui.end_step(self.is_visualisation_on)
                self.master.update()
            if not self.game_is_started:
                break
            if self.player_is_on_pause:
                break
            self.generation_count += 1
            if self.generation_count >= int(self.generations_var.get()) != 0:
                break
            self.generation_count_label['text'] = str(self.generation_count)
            self.world_ui.end_generation(self.is_visualisation_on)

    def player_pause_command(self):
        """

        :return:
        """
        if self.player_is_on_pause:
            self.player_pause['text'] = '||'
            self.player_pause_tooltip.text = "Pause"
            self.player_is_on_pause = False
            self.start_command(True)
        else:
            self.player_pause['text'] = '>'
            self.player_pause_tooltip.text = "Continue"
            self.player_is_on_pause = True


if __name__ == '__main__':
    app = Application()
    app.add_world("First World", FirstWorld)
    app.start()
