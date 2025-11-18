import copy

class StateManager:
    def __init__(self):
        self.history = []


    def push_state(self, board):

        snapshot = copy.deepcopy(board)
        self.history.append(snapshot)


    def undo(self):
        if len(self.history) <= 1:
            return
        self.history.pop()
        current_snapshot = copy.deepcopy(self.history[-1])
        self.history[-1] = current_snapshot


    def get_current_state(self):
        return copy.deepcopy(self.history[-1])

    def reset(self):
        import copy
        if not self.history:
            return
        first = self.history[0]
        self.history = [copy.deepcopy(first)]