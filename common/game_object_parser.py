from common.game_objects import Game, Snake, Board

class GameObjectFactory:
    """
    Creates game objects based on a dictionary of its values
    """

    @staticmethod
    def parse_board(values_dict):
        height = values_dict["height"]
        width = values_dict["width"]
        food = GameObjectFactory.parse_food(values_dict["food"])
        # food = GameObjectFactory.parse_food(values_dict["hazards"])
        snakes = GameObjectFactory.parse_snakes(values_dict["snakes"])
        return Board(height, width, food, snakes=snakes, hazards=None)

    @staticmethod
    def parse_snake(snake):
        snake_id = snake["id"]
        name = snake["name"]
        health = snake["health"]
        latency = snake["latency"]
        body = GameObjectFactory.parse_coordinates(snake["body"])
        head = GameObjectFactory.parse_coordinate(snake["head"])
        length = snake["length"]
        shout = snake["shout"]
        # squad = snake["squad"] # TODO: This does not exist?
        # The color, head_type, tail_type are only sent once to the server.
        # they are not returned again.
        # TODO: We therefore have no representation on how the enemy looks like?
        snake_obj = Snake(snake_id, name, health, body, latency, head, length, shout)
        # snake_obj.Initialise(snake_id, name, health, body, head, length, shout)
        return snake_obj

    @staticmethod
    def parse_snakes(snakes):
        return list(map(lambda snake: GameObjectFactory.parse_snake(snake), snakes))

    @staticmethod
    def parse_coordinate(coord):
        return coord["x"], coord["y"]

    @staticmethod
    def parse_coordinates(coords):
        return list(map(lambda coord: GameObjectFactory.parse_coordinate(coord), coords))

    @staticmethod
    def parse_food(values_dict):
        return GameObjectFactory.parse_coordinates(values_dict)

