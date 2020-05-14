from src.entities.Interactable import Interactable


class Pickupable(Interactable):
    def __init__(self, texture, size, pos, Statistics):
        """
        Create a pickupable object. Pickupable object disappear when interacted with.

        :param texture: Path to a file with the texture
        :param size: Size in px
        :param pos: Position tuple of (x,y)
        :param Statistics: Outcome of the interaction
        """
        super().__init__(texture, size, pos, Statistics)
        self.is_pickupable = True

    def on_interaction(self, Player):
        """
        Applies an outcome to the player and self-destructs.

        :param Player: Player object
        """
        super(Pickupable, self).on_interaction(Player)
        self.kill()
