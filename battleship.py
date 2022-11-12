"""A game of battleships."""

from os import system
from platform import system as operating_system
from string import ascii_uppercase
from time import sleep


class Constants:
    """Globally accessed constants."""

    SHIP_TYPES: dict[str, list[str]] = {
        "carrier": ["X", "X", "X", "X", "X"],
        "battleship": ["X", "X", "X", "X"],
        "destroyer": ["X", "X", "X"],
        "submarine": ["X", "X", "X"],
        "patrol boat": ["X", "X"],
        "speedboat": ["X"]
    }
    COORDS_TRANSLATION: dict[str, int] = dict(
        zip(ascii_uppercase[:5], range(5)))
    VALID_COORDINATES: list[str] = []
    TYPE_OF_FIELD: dict[str, str] = {
        "empty": "O",
        "ship": "X",
        "missed": "M",
        "hit": "H",
        "sunk": "S"
    }
    GAME_MODES: dict[int, str] = {
        1: "Multiplayer",
        2: "Singleplayer against PC"
    }

# game_board = [["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"]]


def generate_board_size(selected_size: int) -> None:
    """Populate game constants with required values."""
    Constants.COORDS_TRANSLATION = dict(
        zip(ascii_uppercase[:selected_size], range(selected_size)))
    Constants.VALID_COORDINATES = [row+str(column) for column in
                                   range(selected_size)
                                   for row in Constants.COORDS_TRANSLATION]


def get_game_mode() -> int:
    """Ask user to select a game mode."""
    selected_mode = 0
    print("Available modes:")
    while selected_mode not in Constants.GAME_MODES:
        for key, value in Constants.GAME_MODES.items():
            print(f"   {key}: {value}")
        try:
            selected_mode = int(input("\nSelect game mode.\n"))
            if selected_mode < 1 or selected_mode > len(Constants.GAME_MODES):
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid number.\n")
    print(f"Selected '{Constants.GAME_MODES[selected_mode]}' mode.")
    return selected_mode


def get_board_size() -> int:
    """Ask user to select a board size."""
    selected_size = 0
    while selected_size not in range(5, 11):
        try:
            selected_size = int(
                input("\nSelect board size between 5 and 10.\n"))
            if selected_size < 5 or selected_size > 10:
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid number.\n")
    print("Generating board...")
    generate_board_size(selected_size)
    sleep(1)
    print(f"Board with size {selected_size} generated.")
    return selected_size


def get_user_coords() -> str:
    pass


def get_ship_direction() -> str:
    pass


def get_ship_type() -> str:
    """Ask user which ship type to place on board."""
    ship_type: str = ""
    while ship_type not in Constants.SHIP_TYPES:
        print("Ship types:")
        for name in Constants.SHIP_TYPES:
            print("   " + name)
        try:
            ship_type = input("\nSelect a type of ship\n")
            if ship_type not in Constants.SHIP_TYPES:
                raise ValueError
        except ValueError:
            print("\nUnknown ship type.\n")
    return ship_type


def validate_coords() -> bool:
    pass


def normalize_coords(user_coords: str) -> str:
    pass


def translate_coords(user_coords: str) -> tuple[int, int]:
    """Convert user input into a format used in the game."""
    converted: list[int] = [
        int(Constants.COORDS_TRANSLATION[user_coords[0]]),
        int(user_coords[1::]) - 1]
    return converted[0], converted[1]


def get_empty_board(board_size: int) -> list[str]:
    pass


def display_board(game_board: list[str]) -> None:
    pass


def check_ship_proximity(game_board: list[str],
                         user_coords: tuple[int, int],
                         ship_type: list[str],
                         ship_direction: str) -> bool:
    """Check if attempt to place a ship has enough space."""
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


def check_for_hit(game_board: list[str],
                  user_coords: tuple[int, int]
                  ) -> list[str]:
    pass  # rename later


def attempt_feedback(hit_miss_sunk: str) -> None:
    pass


def get_winner(game_board: list[str]) -> None:
    pass


if __name__ == "__main__":
    # get_ship_type()
    # print(COORDS_TRANSLATION)
    # print(translate_coords("J2138"))
    # get_game_mode()
    # print(Constants.COORDS_TRANSLATION)
    # print(Constants.VALID_COORDINATES)
    # get_board_size()
    # print(Constants.VALID_COORDINATES)
    # print(Constants.COORDS_TRANSLATION)
    pass
