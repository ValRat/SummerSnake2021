from typing import Tuple, List
from copy import deepcopy

from common.game_objects import Board, Snake
from common.point_utils import get_all_neighbours


# Emulates the game engine, with respect to only one snake - this enables a simpler implementation
# for the multi-minimax algorithm. Since it operates off of Best Reply Search that allows 
# a single opponent to act. This means that the updateStateSingle result can be inconsistent with the 
# "correct" state of the board.
def updateStateSingle(board: Board, snake: Snake, move: Tuple[int, int], validate: bool = True) -> Board:
  next_state = deepcopy(board)

  if validate:
    if not isMoveValid(board, snake, move):
      raise Exception('Invalid move for board')
  
  # Apply snake's chosen move
  board_snake_ref = list(filter(lambda x: x.name == snake.name, board.snakes))[0]
  board_snake_ref.head = move
  board_snake_ref.body.insert(0, move)

  # Handle food consumption
  if move not in board.food:
    board_snake_ref.body.pop() 
    board_snake_ref.health -= 1
    if move in board.hazards:
      board_snake_ref.health -= 15
  else:
    board.food.remove(move)
    board_snake_ref.health = 100
  
  # Place any new food (not implemented in this case)

  # Eliminate any snakes that's been eliminated or removed
  # Since only one snake is modified, we only need 
  # to check whether our snake has been wiped.
  isDead = isOutOfBound(board, move) or isCollidedWithSelf(snake)


  # Need to program logic for: 
  # - the case of when the snake collides head to head
  # - the case when the snake collide with another snake's body

  return next_state

def isOutOfHealth(snake: Snake) -> bool:
  return snake.health <= 0

def isCollidedWithSelf(snake: Snake) -> bool:
  # Check for duplicates in body coordinates
  return len(set(snake.body)) != len(snake.body)

def isCollidedWithAnother(snake: Snake, others: List[Snake]) -> bool:
  # The head is a special case, we evaluate it in another manner
  return False


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