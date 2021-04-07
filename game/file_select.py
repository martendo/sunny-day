import pygame
import tkinter as tk
from tkinter import filedialog
from game.button import Button
from game import colour
from game.game_state import GameState

class FileSelect:
    BUTTON_WIDTH = 600
    BUTTON_HEIGHT = 75
    SPACING = 50
    
    BG_COLOUR = (135, 255, 194)
    
    def __init__(self, game):
        self.game = game
        
        self.OPEN_BUTTON = Button(
            self.game,
            (
                self.game.WIDTH / 2 - (self.BUTTON_WIDTH + self.SPACING / 2),
                self.game.HEIGHT / 2 - self.BUTTON_HEIGHT / 2,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            Button.COLOUR,
            Button.HOVER_COLOUR,
            "Open File",
            colour.BLACK,
            self.open_file,
        )
        self.NEW_BUTTON = Button(
            self.game,
            (
                self.game.WIDTH / 2 + self.SPACING / 2,
                self.game.HEIGHT / 2 - self.BUTTON_HEIGHT / 2,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            ),
            Button.COLOUR,
            Button.HOVER_COLOUR,
            "New File",
            colour.BLACK,
            self.new_file,
        )
    
    def open_file(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(
            parent=root,
            title="Open Save File",
            filetypes=(("Sunny Day! Save File", ".sds"), ("All Files", "*")),
        )
        root.destroy()
        if filename == "":
            return
        self.game.load(filename)
        self.got_file()
    
    def new_file(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename(
            parent=root,
            title="New Save File",
            filetypes=(("Sunny Day! Save File", ".sds"), ("All Files", "*")),
            defaultextension=".sds",
        )
        root.destroy()
        if filename == "":
            return
        self.game.save(filename)
        self.game.load(filename)
        self.got_file()
    
    def got_file(self):
        self.game.screen_fader.start(mid_func=self.done)
    
    def done(self):
        self.game.state = GameState.LEVEL_SELECT
        self.game.LEVEL_SELECT.make_buttons()
    
    def draw(self, surface):
        surface.fill(self.BG_COLOUR)
        
        self.OPEN_BUTTON.draw()
        self.NEW_BUTTON.draw()
