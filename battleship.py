"""A game of battleships."""

from math import inf
from os import system
from platform import system as operating_system
INFINITY = int(inf)
SHIPS: dict[str, list[str]] = {
    "carrier": ["X", "X", "X", "X", "X"],
    "battleship": ["X", "X", "X", "X"],
    "destroyer": ["X", "X", "X"],
    "submarine": ["X", "X", "X"],
    "patrol boat": ["X", "X"],
    "speedboat": ["X"]
}
COORDS_TRANSLATION: dict[str, str] = {
    "A": "0", "B": "1", "C": "2", "D": "3", "E": "4",
    "F": "5", "G": "6", "H": "7", "I": "8", "J": "9"
}
VALID_COORDINATES: list[str] = ["A1", "A2", "A3", "A4", "A5",
                                "B1", "B2", "B3", "B4", "B5",
                                "C1", "C2", "C3", "C4", "C5",
                                "D1", "D2", "D3", "D4", "D5",
                                "E1", "E2", "E3", "E4", "E5"
                                ]
TYPE_OF_FIELD: dict[str, str] = {
    "empty": "O",
    "ship": "X",
    "missed": "M",
    "hit": "H",
    "sunk": "S"
}

GAME_MODES: dict[int, str] = {
    1: "Multiplayer",
    2: "Singleplayer against AI"
}

# game_board = [["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"]]


def get_user_coords() -> str:
    pass


def get_ship_direction() -> str:
    pass


def get_ship_type(ships: dict[str, list[str]]) -> str:
    """Ask user which ship type to place on board."""
    ship_type: str = ""
    while ship_type not in ships.keys():
        print(f"{ships}")
        ship_type = input("Select a type of ship")
    return ship_type


def validate_coords(valid_coordinates: list[str]) -> bool:
    pass


def normalize_coords(user_coords: str) -> str:
    pass


def translate_coords(user_coords: str,
                     coords_dictionary: dict[str, str]
                     ) -> tuple[int, int]:
    """Convert user input into a format used in the game."""
    converted: list[int] = [
        int(coords_dictionary[user_coords[0]]), int(user_coords[1]) - 1]
    return converted[0], converted[1]


def get_empty_board(board_size: int) -> list[str]:
    pass


def display_board(game_board: list[str]) -> None:
    pass


def check_ship_proximity(game_board: list[str],
                         user_coords: tuple[int, int],
                         ship_type: list[str],
                         ship_direction: str) -> bool:
    pass


def waiting_screen(wait_message: str) -> None:
    pass

# input1 = input("Press any key")
# if input1:
#     game_continue()


def clear_terminal() -> None:
    """Terminal cleaning for proper animation display."""
    if operating_system() == "Windows":
        def clear():
            return system("cls")
        clear()  # on Windows systems
    else:
        system("clear")  # on Unix systems


def boards_side_by_side() -> str:
    pass
# DICE = [
#     ("-----",
#      "|   |",
#      "| o |",
#      "|   |",
#      "-----",),
#     ("-----",
#      "|o  |",
#      "|   |",
#      "|  o|",
#      "-----",),  # etc.
# ]


# rolled_dice = (1, 2)

# for i in range(5):  # 5 is the height of the die.
#     for die in rolled_dice:
#         # Now get the corresponding die in the DICE list
#         # and print its first line, then the first line of
#         # the next die and so on.
#         print(DICE[die-1][i], end=' ')
#     print()

def whose_turn_is_it(turn_counter: int) -> str:
    """Get player symbol based on turn number."""
    return "Player 2" if turn_counter % 2 == 0 else "Player 1"


def check_for_hit(game_board: list[str], user_coords: tuple[int, int]) -> list[str]:
    pass  # rename later


def attempt_feedback(hit_miss_sunk: str) -> None:
    pass


def get_winner(game_board: list[str]) -> None:
    pass


if __name__ == "__main__":
    get_ship_type(SHIPS)
    translate_coords("C3", COORDS_TRANSLATION)
