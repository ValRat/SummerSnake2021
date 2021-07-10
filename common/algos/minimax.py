from common.game_objects import Snake, Board
from common.point_utils import get_all_valid_neighbours
from common.heuristics import evaluate

def multi_minimax() -> str:
    return ''


def minimax(me: Snake, enemies: Snake, depth: int, alpha: int, beta: int, isMax: bool, board: Board) -> int:

    # Hmm, is this common enough that we don't need point_utils to be
    # unaware of Game Objects?
    hazards = []

    for snake in board.snakes:
        hazards.extend(snake.body)
    
    valid_neighbours = get_all_valid_neighbours(me.head, hazards, board.height, board.width)
    
    # Termination clause for minimax
    if depth == 0 or len(valid_neighbours) == 0:
        return evaluate(me, board)

    if isMax:
        max_move = float('inf')
        for neighbour in valid_neighbours:



        return 1
    else:
        return 0


    