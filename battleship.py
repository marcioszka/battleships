"""A game of battleships."""

from os import system
from platform import system as operating_system
from string import ascii_uppercase
from time import sleep


class Constants:  # pylint: disable=[too-few-public-methods]
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
    """Populate game constants with size adjusted values."""
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


def confirm_placement():
    """Ask user for confirmation of ship placement."""
    pass


def remove_ship():
    """Remove placed ship from player board."""
    pass


def get_user_coords() -> str:
    """Ask user for coordinates."""
    pass


def get_ship_direction() -> str:
    """Ask user for ship placement plane."""
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
    """Check if input coordinates are withing board bounds."""
    pass


def normalize_coords(raw_coords: str) -> str:
    """Convert user input into a format used in coordinates translation."""
    pass


def translate_coords(raw_coords: str) -> tuple[int, int]:
    """Convert user input into a format used in the game."""
    converted: list[int] = [
        int(Constants.COORDS_TRANSLATION[raw_coords[0]]),
        int(raw_coords[1::]) - 1]
    return converted[0], converted[1]


def check_for_valid_move(defender_visible_board: list[list[str]],
                         converted_coords: tuple[int, int]) -> bool:
    """Check if user defined coordinates are a valid move."""
    row, column = converted_coords[0], converted_coords[1]
    return (defender_visible_board[row][column]
            in ["O", "X"])


def get_empty_board(board_size: int) -> list[list[str]]:
    """Create new playable board."""
    return [["O"]*board_size]*board_size


def display_board(player_board: list[list[str]]) -> str:
    """Convert iterable board into multi line string."""
    pass


def check_ship_proximity(player_board: list[list[str]],
                         converted_coords: tuple[int, int],
                         ship_type: list[str],
                         ship_direction: str) -> bool:
    """Check if ship placement attempt has enough space."""
    pass


def waiting_screen(wait_message: str) -> None:
    """Display message during placement phase when switching players."""
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
    """Display both players visible board versions side by side."""
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


def check_if_sunk():
    """Confirm that a ship has been sunk."""
    pass


def place_move_on_board(defender_visible_board: list[list[str]],
                        defender_hidden_board: list[list[str]],
                        converted_coords: tuple[int, int]
                        ) -> tuple[list[list[str]], list[list[str]]]:
    """Place attack coordinates result on player boards."""
    row, column = converted_coords[0], converted_coords[1]
    hidden_board = defender_hidden_board.copy()
    visible_board = defender_visible_board.copy()
    if hidden_board[row][column] == "X":
        if check_if_sunk():
            move_attempt_feedback("sunk")
            hidden_board[row][column] = "S"
            visible_board[row][column] = "S"
        else:
            move_attempt_feedback("hit")
            hidden_board[row][column] = "H"
            visible_board[row][column] = "H"
    elif hidden_board[row][column] == "O":
        move_attempt_feedback("miss")
        hidden_board[row][column] = "M"
        visible_board[row][column] = "M"
    return hidden_board, visible_board


def move_attempt_feedback(hit_miss_sunk: str) -> None:
    """User feedback based on his move attempt."""
    pass


def check_for_winner(player_board: list[list[str]]) -> tuple[bool, int]:
    """Check if a player won after his last move."""
    pass


def get_winner(player_board: list[list[str]],
               turn: int) -> None:
    """Display a message which player won."""
    pass


if __name__ == "__main__":
    # Testing and execution purpose

    # main()
    # get_ship_type()
    # print(COORDS_TRANSLATION)
    # print(translate_coords("J2138"))
    # get_game_mode()
    # print(Constants.COORDS_TRANSLATION)
    # print(Constants.VALID_COORDINATES)
    # get_board_size()
    # print(Constants.VALID_COORDINATES)
    # print(Constants.COORDS_TRANSLATION)
    print(get_empty_board(10))
    pass
