class State:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.prev_state = None
        self.player_start = None
        self.player_setup = False
        self.map = False

    def update(self, delta_time, actions):
        pass  

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()