from typing import Tuple
from copy import deepcopy

from common.game_objects import Board, Snake
from common.point_utils import get_all_neighbours


# Emulates the game engine
def updateState(board: Board, snake: Snake, move: Tuple[int, int], validate: bool = True) -> Board:
  next_state = deepcopy(board)

  if validate:
    if not isMoveValid(board, snake, move):
      raise Exception('Invalid move for board')
  
  board_snake_ref = list(filter(lambda x: x.name == snake.name, board.snakes))[0]
  board_snake_ref.head = move
  board_snake_ref.body.insert(0, move)


  # Reduce snake length from tail if we didn't eat with the move
  # TODO: Find the cost for each movement and the cost for being in hazard zone
  if move not in board.food:
    board_snake_ref.body.pop() 
    board_snake_ref.health -= 5 
    if move in board.hazards:
      board_snake_ref.health -= 15
  else:
    board.food.remove(move)
    board_snake_ref.health = 100
  
  # Need to program logic for: 
  # - the case of when the snake collide with walls
  # - the case of when the snake collides with other snakes
  # - the case when snake runs out of HP

  return next_state


def isMoveValid(board: Board, snake: Snake, move: Tuple[int, int]) -> bool:
  '''
  Sanity check that the coordinate we're moving into is adjacent to 
  the current snake's head
  ''' 
  return move in get_all_neighbours(snake.head)


def isOutOfBound(board: Board, move: Tuple[int, int]) -> bool:
  def isInBoardBound(point: Tuple[int, int]) -> bool:
    return point[0] >= 0 and point[0] < board.width and point[1] >= 0 and point[1] < board.height
  return not isInBoardBound(move)