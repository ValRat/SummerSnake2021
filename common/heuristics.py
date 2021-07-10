from typing import List, Tuple

from common.game_objects import Board, Snake
from common.point_utils import get_all_neighbours


'''
This class accumulates various heuristics usable with the board state
this is so they may be used across different algos
'''

def is_edge(coordinate: Tuple[int, int], board: Board) -> bool:
    return coordinate[0] == 0 or coordinate[0] == board.width - 1 or coordinate[1] == 0 or coordinate[1] == board.height - 1

def in_hazard_sauce(coordinate: Tuple[int, int], board: Board) -> bool:
    return coordinate in board.hazards

def in_bigger_snake_striking_range(coordinate: Tuple[int, int], me: Snake, board: Board) -> bool:
    other_snakes = list(filter(lambda x : x.name != me.name, board.snakes))
    bigger_snakes = list(filter(lambda x: len(x.body) >= len(me.body), other_snakes))
    bigger_snakes_potential_space_array = map(lambda x : get_all_neighbours(x.head), bigger_snakes)
    bigger_snakes_potential_space: List[Tuple[int, int]] = [item for sublist in bigger_snakes_potential_space_array for item in sublist]
    return coordinate in bigger_snakes_potential_space

# Gives a score evaluation on how good the current state is for
# the given snake
def evaluate(me: Snake, board: Board) -> int:
    return 100

