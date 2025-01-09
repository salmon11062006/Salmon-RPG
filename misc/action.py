from random import randint


class Action:
    def __init__(self, player):
        self.player = player #refers to the player

#controls the mp cost of each spell
class Spell(Action):
    def __init__(self, type, player):
        super().__init__(player)
        self.type = type #for picking between spells

        if self.type == 'Lunge':
            self.mp_cost = 5
        if self.type == 'Heavy Strike':
            self.mp_cost = 7
        if self.type == 'Fireball':
            self.mp_cost = 5
        if self.type == 'Shield Throw':
            self.mp_cost = 3

#amount calculates the damage amount of each spell
    def use(self):
        if self.type == 'Fireball':
            #fireball scales off of INTELLIGENCE
            amount = randint(int(self.player.stats['INT']/2-3), int(self.player.stats['INT']/2+3)) * 2
        elif self.type == 'Heavy Strike':
            #heavy strike scales off of STRENGTH
            amount = randint(int(self.player.stats['STR']/2-3), int(self.player.stats['STR']/2+3)) * 3
        elif self.type == 'Shield Throw':
            #shield throw scales off of VITALITY
            amount = randint(int(self.player.stats['VIT']/2-3), int(self.player.stats['VIT']/2+3)) * 2
        elif self.type == 'Lunge':
            #lunge scales off of AGILITY
            amount = randint(int(self.player.stats['AGI']/2-3), int(self.player.stats['AGI']/2+3)) * 2
        return amount
    
#potion is classified as an action, referring to the player' stats
class Potion(Action):
    def __init__(self, potion_type, player):
        super().__init__(player)
        self.potion_type = potion_type #for picking between health and mana potion

    def use(self):
        if self.potion_type == 'Mana':
            return 30 #amount of mana healed
        elif self.potion_type == 'Health':
            return 30 #amount of health healed
            
#attack is classified as an action, also referring to the player's stats
class Attack(Action):
    def __init__(self, player):
        super().__init__(player)

#amount calculates the damage amount of the melee attack
    def use(self):
        #wanted to add a weapon system, but didn't have enough time to implement :(
        if self.player.weapon:
            amount = self.player.weapon.damage + randint(int(self.player.stats['STR'] / 2 - 3), int(self.player.stats['STR'] / 2 + 3))
        else:
            #melee attacks are scaled off of STRENGTH
            amount = int(randint(int(self.player.stats['STR'] / 2 - 3), int(self.player.stats['STR'] / 2 + 3)))
        return amount