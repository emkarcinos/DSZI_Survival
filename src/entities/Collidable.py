from src.entities.Entity import Entity


class Collidable(Entity):

    def __init__(self, texture, pos, id):
        super().__init__(texture, pos, id)
        self.is_collidable = True


