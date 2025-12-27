from collections import deque
import heapq

class Solver:
    def __init__(self):
        self.visited_nodes = 0
        self.visited = set()
        self.solution=[]

    def solve(self,board, algorithm="dfs"):
        self.visited = set()
        self.solution=[]
        self.visited_nodes=0

        method = getattr(self, algorithm)
        method(board)
        self.solution = self.solution[::-1]

        return  {
        "solution": self.solution,
        "visited" : self.visited_nodes ,
        "moves" : len(self.solution),
        "states": len(self.visited),
        }

    def dfs(self, board):
       state=board.hashed()
       if state in self.visited:
           return False
       self.visited_nodes += 1
       self.visited.add(state)
       if board.GameStatus == "won":
           return True
       if board.GameStatus == "lose" or board.is_goal_surrounded_by_lava():
           return False
       ret=0
       moves=board.get_available_moves()
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
        self.visited = {start_state}
        visited_nodes = 0
        parent = {start_state: (None, None)}

        while queue:
            board = queue.popleft()
            state = board.hashed()
            visited_nodes += 1

            if board.GameStatus == "won":
                self.visited_nodes = visited_nodes
                self.reconstruct_path(parent, state)
                return True

            if board.GameStatus == "lose" or board.is_goal_surrounded_by_lava():
                continue

            for direction, name in board.get_available_moves():
                new_board = board.clone()
                new_board.handleMovment(direction)
                new_state = new_board.hashed()

                if new_state in self.visited:
                    continue

                self.visited.add(new_state)
                parent[new_state] = (state, name)
                queue.append(new_board)

        return False

    def reconstruct_path(self, parent, final_state):

        state = final_state

        while True:
            prev_state, move = parent[state]
            if prev_state is None:
                break
            self.solution.append(move)
            state = prev_state

    def ucs(self, board):

        self.visited = {}
        start_state = board.hashed()
        parent = {start_state: (None, None)}

        pq = []
        heapq.heappush(pq, (board.num_of_lava, board))
        self.visited[start_state] = board.num_of_lava

        while pq:
            cost, board = heapq.heappop(pq)

            self.visited_nodes+=1
            state = board.hashed()
            if cost > self.visited.get(state, cost):
                continue

            self.visited_nodes += 1

            if board.GameStatus == "won":
                self.reconstruct_path(parent, state)
                return True

            if board.GameStatus == "lose" or board.is_goal_surrounded_by_lava():
                continue
            for direction, name in board.get_available_moves():
                new_board = board.clone()
                new_board.handleMovment(direction)
                new_state = new_board.hashed()
                new_cost = cost + new_board.num_of_lava

                if new_cost < self.visited.get(new_state, float("inf")):
                    self.visited[new_state] = new_cost
                    parent[new_state] = (state, name)
                    heapq.heappush(pq, (new_cost, new_board))

        return False

    def Astar(self, board):

        pq=[]
        start_state=board.hashed()
        heapq.heappush(pq, (board.distanceToGoal(), board))
        bestScore = {start_state:0}
        parent = {start_state: (None, None)}
        while pq:
            cost, board = heapq.heappop(pq)
            current_state = board.hashed()
            if current_state in self.visited:
                continue
            self.visited.add(current_state)
            self.visited_nodes += 1

            if board.GameStatus == "won":
                self.reconstruct_path(parent, current_state)
                return True
            if board.GameStatus == "lose" or board.is_goal_surrounded_by_lava():
                continue
            for direction, name in board.get_available_moves():
                new_board = board.clone()
                new_board.handleMovment(direction)
                new_state = new_board.hashed()

                new_cost = bestScore[current_state] + 1
                if new_state not in bestScore or new_cost < bestScore[new_state]:
                    bestScore[new_state] = new_cost
                    parent[new_state] = (current_state, name)
                    heapq.heappush(pq, (new_cost+new_board.distanceToGoal(), new_board))
        return False

    def hill_climb(self, board):
       state=board.hashed()
       if state in self.visited:
           return False
       self.visited_nodes += 1
       self.visited.add(state)
       if board.GameStatus == "won":
           return True
       if board.GameStatus == "lose" or board.is_goal_surrounded_by_lava():
           return False
       ret=0
       moves=board.get_sorted_available_moves()

       for direction , name in moves:
            new_board=board.clone()
            new_board.handleMovment(direction)
            ret = self.hill_climb(new_board)
            if ret:
                self.solution.append(name)
                break
       return ret

