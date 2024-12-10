from random import randint


class Action:
    def __init__(self, player):
        self.player = player

class Spell(Action):
    def __init__(self, type, player):
        super().__init__(player)
        self.type = type

        if self.type == 'Lunge':
            self.mp_cost = 5
        if self.type == 'Heavy Strike':
            self.mp_cost = 7
        if self.type == 'Fireball':
            self.mp_cost = 5
        if self.type == 'Shield Throw':
            self.mp_cost = 3

    def use(self):
        if self.type == 'Fireball':
            amount = randint(int(self.player.stats['INT']/2-3), int(self.player.stats['INT']/2+3)) * 2
        elif self.type == 'Heavy Strike':
            amount = randint(int(self.player.stats['STR']/2-3), int(self.player.stats['STR']/2+3)) * 3
        elif self.type == 'Shield Throw':
            amount = randint(int(self.player.stats['VIT']/2-3), int(self.player.stats['VIT']/2+3)) * 2
        elif self.type == 'Lunge':
            amount = randint(int(self.player.stats['AGI']/2-3), int(self.player.stats['AGI']/2+3)) * 2
        return amount
    
class Potion(Action):
    def __init__(self, potion_type, player):
        super().__init__(player)
        self.potion_type = potion_type

    def use(self):
        if self.potion_type == 'Mana':
            return 10
        elif self.potion_type == 'Health':
            return 50
            

class Attack(Action):
    def __init__(self, player):
        super().__init__(player)

    def use(self):
        if self.player.weapon:
            amount = self.player.weapon.damage + randint(int(self.player.stats['STR'] / 2 - 3), int(self.player.stats['STR'] / 2 + 3))
        else:
            amount = int(randint(int(self.player.stats['STR'] / 2 - 3), int(self.player.stats['STR'] / 2 + 3)))
        return amount