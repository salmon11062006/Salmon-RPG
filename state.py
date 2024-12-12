#this class serves as a transition class to move through functions in different files
class State:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.prev_state = None
        self.player_start = None
        self.player_setup = False
        self.map = False

    def update(self, delta_time, actions): #for update functions in other classes
        pass  

    def render(self, surface): #for render functions in other classes
        pass

    def enter_state(self): #for entering a state
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop() #exits the state