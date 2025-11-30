from collections import deque

class Solver:
    def __init__(self):
        self.visited_nodes = 0
        self.visited = set()
        self.solution=[]

    ## I used that function because name of algo passed from gui
    def solve(self,board, algorithm="dfs"):
        self.visited = set()
        self.solution=[]
        self.visited_nodes=0
        if algorithm == "dfs":
            self.dfs(board)
        else:
            self.bfs(board)

        self.solution = self.solution[::-1]
        return  {
        "solution": self.solution,
        "visited" : self.visited_nodes ,
        "moves" : len(self.solution),
        "states": len(self.visited),
        }



    def dfs(self, board):
       state=board.hashed()
       if state in self.visited or board.number_of_moves >= 200:
           return False
       self.visited_nodes += 1
       self.visited.add(state)
       if board.GameStatus == "won":
           return board.number_of_moves
       if board.GameStatus == "lose" :
           return False
    ## boolean denote if got an answer or not
       ret=0
       moves=board.get_available_moves()
    ## name is like (left ) i used it just for printing
       for direction , name in moves:
            new_board=board.clone()
            new_board.handleMovment(direction)
            ret = self.dfs(new_board)
            if ret:
                self.solution.append(name)
                break
       return ret

    def bfs(self, start_board):
        start_state = start_board.hashed()

        queue = deque([start_board])
        self.visited = set([start_state])
        visited_nodes=0
        parent = {start_state: (None, None)}

        while queue:
            board = queue.popleft()
            state = board.hashed()
            visited_nodes+=1
            if board.GameStatus == "won" :
                self.visited_nodes=visited_nodes
                self.reconstruct_path(parent, state)
                return board.number_of_moves
            if board.GameStatus == "lose"  or board.number_of_moves > 100 :
                continue
            for direction, name in board.get_available_moves():
                new_board = board.clone()
                new_board.handleMovment(direction)
                new_state = new_board.hashed()

                if new_state not in self.visited:
                    self.visited.add(new_state)

                    parent[new_state] = (state, name)
                    queue.append(new_board)
        return 0

    def reconstruct_path(self, parent, final_state):

        state = final_state

        while True:
            prev_state, move = parent[state]
            if prev_state is None:
                break
            self.solution.append(move)
            state = prev_state

