from src.entities.Entity import Entity


class Collidable(Entity):

    def __init__(self, texture, pos, id):
        super().__init__(texture, pos, id)

    def check_for_collision(self, x_pos, y_pos):
        if self.pos[0] == x_pos:
            if self.pos[1] == y_pos:
                return True

        return False


col = Collidable(1, 1, 1)


"""
    def interact_with_hp(self, hp, Statistics):
        Statistics.set_hp(hp)

    def interact_with_hunger(self, hunger, Statistics):
        Statistics.set_hunger(hunger)

    def interact_with_thirst(self, thirst, Statistics):
        Statistics.set_thirst(thirst)

    def interact_with_stamina(self, stamina, Statistics):
        Statistics.set_stamina(stamina)"""