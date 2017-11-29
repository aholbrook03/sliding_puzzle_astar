# Filename: sliding_puzzle_astar.py
# By: Andrew Holbrook
# Date: 9/30/2016

# implementation of A* for solving the sliding puzzle
def solve_puzzle(puzzle):

    # check that there is an empty tile
    if find_empty_tile(puzzle) == None:
        print("No empty tile found!")
        return False

    # list of visited node (puzzle states)
    closed_list = []

    # store puzzle states as a tuple of tuples
    open_list = [tuple([tuple(x) for x in puzzle])]

    # cost of going from starting puzzle to current puzzle
    g_score = {open_list[0] : 0}

    # cost of going to starting puzzle to current puzzle, plus the cost of
    # going from the current puzzle to the goal
    f_score = {open_list[0] : heuristic(open_list[0])}

    # keep track of moves
    came_from = {}

    while len(open_list) > 0:

        # get puzzle with the smallest fscore from open_list
        current_puzzle = min([(f_score[x], x) for x in open_list])[1]

        # check if we've solved the puzzle
        if heuristic(current_puzzle) == 0:
            return construct_path(came_from, current_puzzle)

        open_list.remove(current_puzzle)
        closed_list.append(current_puzzle)

        for neighbor in get_neighbors(current_puzzle):
            if neighbor in closed_list:
                continue

            tmp_g_score = g_score[current_puzzle] + 1

            if neighbor not in open_list:
                open_list.append(neighbor)
            elif tmp_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current_puzzle
            g_score[neighbor] = tmp_g_score
            f_score[neighbor] = tmp_g_score + heuristic(neighbor)

    return False

# get list of moves from initial puzzle state to the goal
def construct_path(came_from, final_puzzle):
    path = [final_puzzle]
    current_puzzle = final_puzzle
    while current_puzzle in came_from:
        current_puzzle = came_from[current_puzzle]
        path.append(current_puzzle)

    path.reverse()
    return path

def find_empty_tile(puzzle):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] == -1:
                return (x, y)
    return None

# return a list possible puzzle states after one move given the current state
def get_neighbors(puzzle):
    neighbors = []
    empty_tile = find_empty_tile(puzzle)

    if empty_tile[0] - 1 >= 0:
        neighbors.append(swap_tiles(puzzle, empty_tile,
            (empty_tile[0] - 1, empty_tile[1])))
    if empty_tile[0] + 1 < len(puzzle[0]):
        neighbors.append(swap_tiles(puzzle, empty_tile,
            (empty_tile[0] + 1, empty_tile[1])))
    if empty_tile[1] - 1 >= 0:
        neighbors.append(swap_tiles(puzzle, empty_tile,
            (empty_tile[0], empty_tile[1] - 1)))
    if empty_tile[1] + 1 < len(puzzle):
        neighbors.append(swap_tiles(puzzle, empty_tile,
            (empty_tile[0], empty_tile[1] + 1)))

    return neighbors

def swap_tiles(puzzle, tile_a, tile_b):
    tmp_puzzle = list([list(x) for x in puzzle])
    tmp_tile = tmp_puzzle[tile_a[1]][tile_a[0]]
    tmp_puzzle[tile_a[1]][tile_a[0]] = tmp_puzzle[tile_b[1]][tile_b[0]]
    tmp_puzzle[tile_b[1]][tile_b[0]] = tmp_tile

    return tuple([tuple(x) for x in tmp_puzzle])

def print_puzzle(puzzle):
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] == -1:
                print('  ', end='')
            else:
                print(str(puzzle[y][x]) + ' ', end='')

        print()

# calculate distance of current puzzle state from goal using Manhattan distance
def heuristic(puzzle):
    result = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if puzzle[y][x] == -1:
                continue

            # use modulo and integer division to find x and y, respectively
            goal_pos = (puzzle[y][x] % 3, puzzle[y][x] // 3)
            result += abs(goal_pos[0] - x) + abs(goal_pos[1] - y)

    return result

# initiale puzzle state
sliding_puzzle = [[7,  2, 4],
                  [5, -1, 6],
                  [8,  3, 1]]

# solve and print moves made from initial to goal
result = solve_puzzle(sliding_puzzle)
if result:
    for puzzle in result:
        print_puzzle(puzzle)
        print()

    # List of moves (stored in result list) also contains the initial state,
    # so subtract 1 to get the total number of moves
    print('Solved in', len(result) - 1, 'moves')
else:
    print("Could not solve puzzle!")
