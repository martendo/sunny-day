import tkinter as tk
from tkinter import filedialog
from game.save import SaveDataError
from game.button import Button
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
            "Open File",
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
            "New File",
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
        try:
            self.game.load(filename)
        except SaveDataError:
            # Invalid save file, ignore
            return
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
    def show(self):
        self.game.state = GameState.FILE_SELECT
        self.OPEN_BUTTON.enabled = True
        self.NEW_BUTTON.enabled = True
    def done(self):
        self.game.LEVEL_SELECT.show()
        self.OPEN_BUTTON.enabled = False
        self.NEW_BUTTON.enabled = False
    
    def draw(self, surface):
        surface.fill(self.BG_COLOUR)
        
        self.OPEN_BUTTON.draw(surface)
        self.NEW_BUTTON.draw(surface)
