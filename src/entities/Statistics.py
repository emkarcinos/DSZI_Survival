class Statistics:
    def __init__(self, hp, hunger, thirst, stamina):
        """
        Create a statistic object. Used to determine some object state (usually player's).

        :param hp: Health points
        :param hunger: Hunger (it rises)
        :param thirst: Thirst (also rises)
        :param stamina: Stamina points that decrease.
        """
        self.hp = hp
        self.hunger = hunger
        self.thirst = thirst
        self.stamina = stamina

    """
    methods that don't let the values pass below 0 and over 100 during change
    """

    def set_hp(self, hp_diff):
        """
        Setter method for setting HP.

        :param hp_diff: Difference as integer
        """
        if 0 <= self.hp + hp_diff <= 100:
            self.hp = self.hp + hp_diff
        else:
            if self.hp + hp_diff <= 0:
                self.hp = 0
            else:
                self.hp = 100

    def set_hunger(self, hunger_diff):
        """
        Setter method for setting hunger points.

        :param hunger_diff: Difference as integer
        """
        if 0 <= self.hunger + hunger_diff <= 100:
            self.hunger = self.hunger + hunger_diff
        else:
            if self.hunger + hunger_diff <= 0:
                self.hunger = 0
            else:
                self.hunger = 100

    def set_thirst(self, thirst_diff):
        """
        Setter method for setting thirst.

        :param thirst_diff: Difference as integer
        """
        if 0 <= self.thirst + thirst_diff <= 100:
            self.thirst = self.thirst + thirst_diff
        else:
            if self.thirst + thirst_diff <= 0:
                self.thirst = 0
            else:
                self.thirst = 100

    def set_stamina(self, stamina_diff):
        """
        Setter method for setting stamina points.

        :param stamina_diff: Difference as integer
        """
        if 0 <= self.stamina + stamina_diff <= 100:
            self.stamina = self.stamina + stamina_diff
        else:
            if self.stamina + stamina_diff <= 0:
                self.stamina = 0
            else:
                self.stamina = 100
