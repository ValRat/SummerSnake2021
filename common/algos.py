from typing import Callable, Dict, Tuple, List
from heapq import heapify, heappush, heappop
from functools import total_ordering

from common.point_utils import get_all_valid_neighbours


# aka gScore, saves the cost of path from start to known universe
class StoredScores(dict):
    def __missing__(self, key):
        return float('inf')


# For ease of storing within the minheap
@total_ordering
class PointWithCost:

    def __init__(self, point: Tuple[int, int], cost: int):
        self.point = point
        self.cost = cost

    def __eq__(self, other):
        return self.cost == other.cost
    
    def __ne__(self, other):
        return self.cost != other.cost
    
    def __gt__(self, other):
        return self.cost > other.cost

    def __str__(self):
        return f'Point: {self.point} | Cost: {self.cost}'

# Reconstructs the path from goal to initial location
def reconstruct_path(cameFrom: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]:
    total_path: List[Tuple[int, int]] = []
    total_path.append(current)
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return list(reversed(total_path))

# This is dumb, optimize if needed
def minheap_contains(heap: List[PointWithCost], point: Tuple[int, int]) -> bool:
    return point in map(lambda p : p.point, heap)

# Stolen from wikipedia
def a_star(start: Tuple[int,int], goal: Tuple[int, int], hazards: List[Tuple[int,int]] = [], height: int = 5, width: int = 5, h: Callable = lambda x : 0) -> List[Tuple[int, int]]: 

    # TODO: make this a little more defined? 
    # Weight function between adjacent nodes
    def d(node_from: Tuple[int, int], node_to: Tuple[int, int]) -> int: 
        return 1
    
    # print(f'Start: {start}, Goal: {goal}')

    openSet: List[PointWithCost] = []
    heapify(openSet)
    heappush(openSet, PointWithCost(start, 0))

    cameFrom: Dict[Tuple[int, int], Tuple[int, int]] = {}

    gScore = StoredScores()
    gScore[start] = 0

    fScore = StoredScores()
    fScore[start] = h(start)

    while len(openSet) > 0: 
        current = heappop(openSet).point
        # print(f'Current: {current}')

        if (current == goal):
            # print(f'Reached goal')
            return reconstruct_path(cameFrom, current)

        # This list shouldn't include actual hazards, no
        neighbours = get_all_valid_neighbours(current, hazards, height, width)
        # print(f'Neighbours: {neighbours} ')
        
        for neighbour in neighbours:
            # print(f'Neighbour: {neighbour} ')
            tentative_gScore = gScore[current] + d(current, neighbour)
            if tentative_gScore < gScore[neighbour]:
                cameFrom[neighbour] = current
                gScore[neighbour] = tentative_gScore
                fScore[neighbour] = gScore[neighbour] + h(neighbour)
                if not minheap_contains(openSet, neighbour):
                    neighbour_pwc = PointWithCost(neighbour,fScore[neighbour])
                    # print(f'Adding Neighbour: {neighbour_pwc} ')
                    heappush(openSet, PointWithCost(neighbour, fScore[neighbour]))

    # TODO: better exception/error handling 
    raise Exception('No valid path found')


# Testing purposes

if __name__ == '__main__':
    openSet: List[PointWithCost] = []
    randopoint = (1, 1)
    heapify(openSet)
    heappush(openSet, PointWithCost(randopoint, 0))
    heappush(openSet, PointWithCost(randopoint, 50))
    heappush(openSet, PointWithCost(randopoint, 99))
    heappush(openSet, PointWithCost(randopoint, 30))
    heappush(openSet, PointWithCost(randopoint, 40))
    heappush(openSet, PointWithCost(randopoint, 33))
    heappush(openSet, PointWithCost(randopoint, 10))

    should_contain = minheap_contains(openSet, (1, 1))
    should_not_contain = minheap_contains(openSet, (1, 2))

    print(f'should_contain: {should_contain}, should_not_contain: {should_not_contain}')
     

