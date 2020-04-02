from src.entities.Entity import Entity


class Collidable(Entity):

    def check_for_collision(self, x_pos, y_pos):
        if self.pos[0] == x_pos:
            if self.pos[1] == y_pos:
                return True

        return False
