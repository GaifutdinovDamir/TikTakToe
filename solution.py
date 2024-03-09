from tictac import Game 
import json
import os.path

graph = dict()
reward = dict()


game = Game()
start = ''.join(map(str, game.field.copy().reshape(-1)))


def dfs(curr_state):
    graph[curr_state] = []

    for i in range(3):
        for j in range(3):
            if game.field[i][j] == 0:
                f, s, draw = game.next_move((i, j))
                new_state = ''.join(map(str, game.field.copy().reshape(-1)))
                graph[curr_state].append((new_state, (i, j)))
                if new_state in graph:
                    game.rollback_move((i, j))
                    continue

                if f:
                    reward[new_state] = 1
                elif s:
                    reward[new_state] = -1
                elif draw:
                    reward[new_state] = 0
                else:
                    dfs(new_state)
                game.rollback_move((i, j))
    if curr_state not in reward:
        if game.moves % 2 == 0:
            f = max
            curr_f = -10
        else:
            f = min
            curr_f = 10
        for state, move in graph[curr_state]:
            curr_f = f(curr_f, reward[state])
        reward[curr_state] = curr_f

dfs(start)

#save dictionary as json file

parentdir = os.path.dirname(os.path.abspath(__file__))
path1 = os.path.join(parentdir, 'graph.json')
path2 = os.path.join(parentdir, 'reward.json')
f1 = open(path1, 'w')
f2 = open(path2, 'w')
json.dump(graph, f1)
json.dump(reward, f2)

