from enum import Enum
from typing import List

class Game:

  def __init__(self, id, timeout):
    self.id = id
    self.timeout = timeout


class Snake:

  def __init__(self, id, name, health, body, latency, head, length, shout, squad = None):
    self.id = id
    self.name = name
    self.health = health
    self.body = body
    self.latency = latency
    self.head = head
    self.length = length
    self.shout = shout
    self.squad = squad



class Board: 

  def __init__(self, height, width, food, hazards, snakes):
    self.height = height
    self.width = width
    self.food = food
    self.hazards = hazards
    self.snakes = snakes
   

# TODO: how to access the values of this, don't think I'm doing it right
class Direction(Enum):
    LEFT = "left",
    RIGHT = "right",
    UP = "up",
    DOWN = "down"


moves = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
