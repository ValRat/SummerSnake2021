import random
from typing import List, Tuple

from common.game_objects import Game, Snake, Board, Direction
from common.algos import a_star
from common.point_utils import get_all_valid_neighbours, get_manhattan_distance

def move_to_valid(me: Snake, board: Board) -> str:
  # Avoid corners
  # Should try and avoid corners if possible somewhat, maybe if it's the only possible option we keep it...
  # hazards = [(0,0), (board.width - 1, 0), (0, board.height - 1), (board.width - 1, board.height - 1) ]
  # hazards.extend(me.body)


  # Ends up colliding with itself a lot... have to program a better heuristic lol
  hazards = me.body

  # Avoid other snakes
  for others in board.snakes: 
    hazards.extend(others.body)
  
  head_coordinate = me.head

  def is_edge(coordinate: Tuple[int, int]) ->  bool:
    return coordinate[0] == 0 or coordinate[0] == board.width - 1 or coordinate[1] == 0 or coordinate[1] == board.height - 1
  
  def in_hazard_sauce(coordinate: Tuple[int, int]) -> bool:
    return coordinate in board.hazards

  # Make it more expensive to straddle edges and being in the hp draining zone
  def heuristic(coordinate: Tuple[int,int]):
    cost = 0
    cost += 5 if is_edge(coordinate) else 0
    cost += 2 if in_hazard_sauce(coordinate) else 0
    return cost

  
  # First food item
  # TODO: Closest food item?
  # Multiple instances of my snake on the same board will target the same food item
  # Not an issue on just a single snake instance

  # Perhaps implement a path-following where, we 
  # iteratively follow get_path and not have to recalculate everything again
  # Try and use the game_id for this
  # i.e. become stateful

  target = best_food_heuristic(me, board)
  next_step = (0, 0)

  try: 
    get_path = a_star(me.head, target, hazards, board.height, board.width, heuristic)
    next_step = get_path[1]
  except Exception:
    # A* failed to find path, find closest valid coordinate
    neighbours = get_all_valid_neighbours(head_coordinate, hazards, board.height, board.width)
    next_step = seek_food_simple(neighbours, board.food)
  # print(f'Current path: {"".join(map(lambda tpl: str(tpl), get_path))}')
  # print(f'Next step: {next_step}')


  # valid_coordinate = random.choice(c3)
  # best_coordinate = seek_food_simple(c3, board.food)

  return get_direction(head_coordinate, next_step)

def best_food_heuristic(me: Snake, board: Board) -> Tuple[int, int]:
  if me.health < 30: 
    # Avoid food that is in the hazard sauce
    def not_in_sauce(coord: Tuple[int, int]) -> bool:
      return coord not in board.hazards
    safe_food = list(filter(not_in_sauce, board.food))
    if len(safe_food) > 0:
      return closest_food_item(me.head, safe_food)

  # No choice
  return closest_food_item(me.head, board.food)

def closest_food_item(coordinate: Tuple[int, int], food: List[Tuple[int,int]]) -> Tuple[int, int]:
  minimum_distance = float('inf')
  closest_food = food[0]
  for nibble in food:
    distance_to_nibble = get_manhattan_distance(coordinate, nibble)
    if distance_to_nibble < minimum_distance:
      closest_food = nibble
      minimum_distance = distance_to_nibble
  return closest_food

def seek_food_simple(coordinates: List[Tuple[int, int]], food: List[Tuple[int,int]]) -> Tuple[int, int]:
  if len(coordinates) == 0: 
    print(f'No possible coordinates')
    return (0, 0)
  # Find smallest distance between food and coordinate
  closest_coordinate_to_food = coordinates[0]
  shortest_distance = float('inf')
  for point in coordinates: 
    for nibble in food:
      print(f'Point: {point} to Food: {nibble}')
      current_distance = abs(nibble[0] - point[0]) + abs(nibble[1] - point[1]) 
      if current_distance < shortest_distance:
        closest_coordinate_to_food = point
        shortest_distance = current_distance
  return closest_coordinate_to_food

def prune_obstacles(coordinates: List[Tuple[int, int]], obstacles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  # There's probably a stdlib for this
  def clear(coord: Tuple[int, int]):
    return coord not in obstacles
  return list(filter(clear, coordinates))


# Valid except for diagonals
# 0,0 defined as bottom left corner
def get_direction(coord_from: Tuple[int, int], coord_to: Tuple[int, int]) -> str: 
  if (coord_from[0] != coord_to[0]): 
    return Direction.RIGHT.name if coord_to[0] > coord_from[0] else Direction.LEFT.name
  else:
    return Direction.UP.name if coord_to[1] > coord_from[1] else Direction.DOWN.name