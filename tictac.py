import numpy as np 
import random
import os.path
import json


class Game():
    def __init__(self):
        self.field = np.zeros(shape=(3, 3), dtype=int)
        self.moves = 0
        
    def next_move(self, move):
        first_won = False
        second_won = False
        if self.moves % 2 == 0 and self.field[move[0], move[1]] == 0:
            self.field[move[0], move[1]] = 1
        elif self.moves % 2 == 1 and self.field[move[0], move[1]] == 0:
            self.field[move[0], move[1]] = -1
        else:
            self.moves -= 1
        self.moves += 1


        def smbd_won(value):
            return (self.field.sum(axis = 0) == value).any() or \
                    (self.field.sum(axis = 1) == value).any() or \
                    (np.trace(self.field) == value) or (np.trace(self.field[::-1, ]) == value)

        if smbd_won(3):
            first_won = True
        if smbd_won(-3):
            second_won = True

        draw = False
        if not first_won and not second_won and self.moves == 9:
            draw = True
        
        return first_won, second_won, draw

    def rollback_move(self, move):
        if self.field[move[0], move[1]] != 0:
            self.field[move[0], move[1]] = 0
            self.moves -= 1

    def print_field(self):
        for row in self.field:
            print(*row, sep = ' ')
    

class Agent():
    def __init__(self, stategraph, rewardgraph, white):
        self.white = white
        self.graph = stategraph
        self.reward = rewardgraph
        if white:
            self.f = max
            self.br = -1
        else:
            self.f = min
            self.br = 1
    
    def make_move(self, state):
        state = ''.join(map(str, state.reshape(-1).copy()))

        best_moves = []
        best_reward = self.br

        #finding best reward
        for st, move in self.graph[state]:
            best_reward = self.f(best_reward, self.reward[st])
        
        #finding possible states to go
        for st, move in self.graph[state]:
            if self.reward[st] == best_reward:
                best_moves.append(move)
        
        #randomly choosing a move
        return random.choice(best_moves)

def main():
    parentpath = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.join(parentpath, 'graph.json')
    path2 = os.path.join(parentpath, 'reward.json')

    f1 = open(path1, 'r')
    f2 = open(path2, 'r')

    graph = json.load(f1)
    reward = json.load(f2)

    game = Game()
    agent = Agent(graph, reward, white = False)

    game.print_field()
    while True:
        move = list(map(int, input().split()))
        first_won, second_won, draw = game.next_move(move)
        game.print_field()
        if first_won:
            print('first won!')
            break
        elif second_won:
            print('second won!')
            break
        elif draw:
            print('draw!')
            break
        
        f, s, draw = game.next_move(agent.make_move(game.field))
        if f:
            print('first won!')
            break
        elif s:
            print('second won!')
            break
        elif draw:
            print('draw!')
            break
        game.print_field()

if __name__ == '__main__':
    main()
