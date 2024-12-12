from misc.level import Level, OrcLevel

#image layers for the map and collision
layers = {
            'ground': 0,
            'player': 1,
            'trees': 2
        }

DISPLAY_W, DISPLAY_H = 800, 400 #display width and height

#enemy levels and stats
big1 = OrcLevel(1, [3,5], 10, 30, [4,8], [5,10])
big2 = OrcLevel(2, [4,7], 12, 40, [8,12], [8,14])
big3 = OrcLevel(3, [6, 10], 14, 50, [13, 17], [12, 18])

big_levels = [big1, big2, big3]

#same thing but for smaller orcs
small1 = OrcLevel(1, [1,4], 4, 15, [2,4], [2,6])
small2 = OrcLevel(2, [3,5], 6, 20, [5,9], [4,10])
small3 = OrcLevel(3, [5,8], 7, 25, [10,14], [8,15])

small_levels = [small1, small2, small3]

#same thing
med1 = OrcLevel(1, [2,6], 6, 20, [3,7], [4,8])
med2 = OrcLevel(2, [4,7], 8, 30, [6,10], [6,12])
med3 = OrcLevel(3, [6,9], 10, 35, [11,15], [10,16])

med_levels = [med1, med2, med3]

#player levels
level0 = Level(0, 15)
level1 = Level(1, 30)
level2 = Level(2, 45)
level3 = Level(3, 60)

player_levels = [level0, level1, level2, level3]