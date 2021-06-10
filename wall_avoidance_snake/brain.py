from common.game_objects import Game, Snake, Board, Direction

def move_to_valid(me: Snake, board: Board) -> str:
  # Avoid corneres
  hazards = [(0,0), (board.width - 1, 0), (0, board.height - 1), (board.width - 1, board.height - 1) ]
  hazards.extend(me.body)
  
  head_coordinate = me.head
  print(hazards)

  c1 = get_surrounding_coordinates(head_coordinate)
  c2 = prune_bound(c1, board.height, board.width)
  c3 = prune_obstacles(c2, hazards)

  first_valid_coordinate = c3[0]

  return get_direction(head_coordinate, first_valid_coordinate)


def get_surrounding_coordinates(origin: (int, int)) -> [(int, int)]:
  return [
    (origin[0]+1, origin[1]),
    (origin[0]-1, origin[1]),
    (origin[0], origin[1]+1),
    (origin[0], origin[1]-1),
  ]

# TODO: In python filter returns an iterable, make this work
def prune_bound(coordinates: [(int, int)], height: int, width: int) -> [(int, int)]:
  def in_bound(coord: (int, int)):
    return coord[0] >= 0 and coord[1] >= 0 and coord[0] < width and coord[1] < height
  return list(filter(in_bound, coordinates))


def prune_obstacles(coordinates: [(int, int)], obstacles: [(int, int)]) -> [(int, int)]:
  # There's probably a stdlib for this
  def clear(coord: (int, int)):
    return coord not in obstacles
  return list(filter(clear, coordinates))


# Valid except for diagonals
# 0,0 defined as bottom left corner
def get_direction(coord_from: (int, int), coord_to: (int, int)) -> str: 
  if (coord_from[0] != coord_to[0]): 
    return Direction.RIGHT.name if coord_to[0] > coord_from[0] else Direction.LEFT.name
  else:
    return Direction.UP.name if coord_to[1] > coord_from[1] else Direction.DOWN.name