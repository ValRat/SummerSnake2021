from typing import Tuple, List

def get_all_neighbours(origin: Tuple[int, int]) -> List[Tuple[int, int]]:
  return [
    (origin[0]+1, origin[1]),
    (origin[0]-1, origin[1]),
    (origin[0], origin[1]+1),
    (origin[0], origin[1]-1),
  ]

def get_manhattan_distance(point1: Tuple[int, int], point2: Tuple[int, int]):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def prune_bound(coordinates: List[Tuple[int, int]], height: int, width: int) -> List[Tuple[int, int]]:
  def in_bound(coord: Tuple[int, int]):
    return coord[0] >= 0 and coord[1] >= 0 and coord[0] < width and coord[1] < height
  return list(filter(in_bound, coordinates))

def prune_obstacles(coordinates: List[Tuple[int, int]], obstacles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
  # There's probably a stdlib for this
  def clear(coord: Tuple[int, int]):
    return coord not in obstacles
  return list(filter(clear, coordinates))

def get_all_valid_neighbours(origin: Tuple[int, int], hazards: List[Tuple[int,int]] = [], height: int = 5, width: int = 5) -> List[Tuple[int, int]]:
    all_neighbours = get_all_neighbours(origin)
    all_neighbours_within_bound = prune_bound(all_neighbours, height, width)
    all_neighbour_within_bound_no_obstacles = prune_obstacles(all_neighbours_within_bound, hazards)
    return all_neighbour_within_bound_no_obstacles #yuck