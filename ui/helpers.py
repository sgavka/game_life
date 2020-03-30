"""
UI helpers
"""

import tkinter as tk


class ToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

        self.top_window = None

    def enter(self, event=None):
        """

        :param event:
        :return:
        """
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.widget.winfo_width()
        y += self.widget.winfo_rooty() + int(self.widget.winfo_height() / 2)

        # creates a toplevel window
        self.top_window = tk.Toplevel(self.widget)

        # leaves only the label and removes the app window
        self.top_window.wm_overrideredirect(True)
        self.top_window.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.top_window, text=self.text, justify='left',
                         background='white', relief='solid', borderwidth=1,
                         font=("times", "12", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        """

        :param event:
        :return:
        """
        if self.top_window:
            self.top_window.destroy()
