from collections import deque

def solve_eight_puzzle(initial_state):
    goal_state = "12345678x"
    moves = [1, -1, 3, -3]
    initial_state = ''.join(initial_state.split())
    queue = deque([(initial_state, 0)])
    visited = set([initial_state])
    while queue:
        state, steps = queue.popleft()
        if state == goal_state:
            return steps
        x_pos = state.index('x')
        for move in moves:
            new_pos = x_pos + move
            if 0 <= new_pos < 9 and abs(x_pos % 3 - new_pos % 3) <= 1:
                new_state = list(state)
                new_state[x_pos], new_state[new_pos] = new_state[new_pos], new_state[x_pos]
                new_state = ''.join(new_state)
                if new_state not in visited:
                    queue.append((new_state, steps + 1))
                    visited.add(new_state)
    return -1

initial_state = input()
steps = solve_eight_puzzle(initial_state)
print(steps)