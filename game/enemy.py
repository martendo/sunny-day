from game.actor import Actor

class Enemy(Actor):
    layer = 0


from game.enemies.renky import Renky

TYPES = {
    "Renky": Renky,
}
