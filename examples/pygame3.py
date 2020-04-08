import sys
import os
import tkinter as tkinter
import pygame


class Game(object):
    def __init__(self, root, w, h):
        self.root = root
        self.width = w
        self.height = h

        # Tk init
        self.frame = tkinter.Frame(root, width=w, height=h)
        self.frame.grid(row=0, columnspan=2)
        self.button1 = tkinter.Button(
            root, text='-', command=lambda: self.incr_step(-1))
        self.button1.grid(row=1, column=0)
        self.button2 = tkinter.Button(
            root, text='+', command=lambda: self.incr_step(1))
        self.button2.grid(row=1, column=1)
        root.update()

        # pygame init
        os.environ['SDL_WINDOWID'] = str(self.frame.winfo_id())
        if sys.platform == "win32":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        self.screen = pygame.display.set_mode((w, h))
        self.bg_color = pygame.Color(0, 0, 0)
        self.fg_color = pygame.Color(255, 255, 255)
        self.position = 0
        self.step = 1

        self.game_loop()

    def game_loop(self):
        self.screen.fill(self.bg_color)
        self.position = (self.position + self.step) % self.width
        coord = self.position, self.height // 2
        pygame.draw.circle(self.screen, self.fg_color, coord, 20)
        pygame.display.flip()

        # self.frame.after(5, self.game_loop)

    def incr_step(self, inc):
        self.step += inc
        self.game_loop()


if __name__ == "__main__":
    root = tkinter.Tk()
    game = Game(root, 200, 200)
    root.mainloop()
