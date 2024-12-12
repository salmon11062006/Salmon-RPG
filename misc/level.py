#both classes are just there to store data for config.py
class OrcLevel:
    def __init__(self, level, dmg_range, speed, max_hp, xp_range, gold_range):
        self.level = level
        self.damage_range = dmg_range
        self.speed = speed
        self.max_hp = max_hp
        self.xp_range = xp_range
        self.gold_range = gold_range

class Level:
    def __init__(self, level, xp):
        self.level = level
        self.xp = xp
