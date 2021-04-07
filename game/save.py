import pickle

class SaveReader:
    def __init__(self, game):
        self.game = game
    
    def load(self, filename):
        self.game.savefile = filename
        with open(self.game.savefile, "rb") as file:
            data = pickle.load(file)
        self.game.last_completed_level = data["last_completed_level"]
        self.game.player.lives = data["lives"]
        self.game.player.coins = data["coins"]
    
    def save(self, filename=None):
        if filename is not None:
            self.game.savefile = filename
        data = {
            "last_completed_level": self.game.last_completed_level,
            "lives": self.game.player.lives,
            "coins": self.game.player.coins,
        }
        with open(self.game.savefile, "wb") as file:
            pickle.dump(data, file)
