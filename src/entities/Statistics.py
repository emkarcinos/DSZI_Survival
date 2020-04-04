class Statistics:
    def __init__(self, hp, hunger, thirst, stamina):
        self.hp = hp
        self.hunger = hunger
        self.thirst = thirst
        self.stamina = stamina

    # methods that don't let the values pass below 0 and over 100 during change
    def set_hp(self, hp_diff):
        if 0 <= self.hp + hp_diff <= 100:
            self.hp = self.hp + hp_diff
        else:
            if self.hp + hp_diff <= 0:
                self.hp = 0
            else:
                self.hp = 100

    def set_hunger(self, hunger_diff):
        if 0 <= self.hp + hunger_diff <= 100:
            self.hp = self.hp + hunger_diff
        else:
            if self.hp + hunger_diff <= 0:
                self.hp = 0
            else:
                self.hp = 100

    def set_thirst(self, thirst_diff):
        if 0 <= self.hp + thirst_diff <= 100:
            self.hp = self.hp + thirst_diff
        else:
            if self.hp + thirst_diff <= 0:
                self.hp = 0
            else:
                self.hp = 100

    def set_stamina(self, stamina_diff):
        if 0 <= self.hp + stamina_diff <= 100:
            self.hp = self.hp + stamina_diff
        else:
            if self.hp + stamina_diff <= 0:
                self.hp = 0
            else:
                self.hp = 100



