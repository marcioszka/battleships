"""A game of battleships."""

from os import system
from platform import system as operating_system
from random import randint
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
    SHIP_DIRECTION: dict[int, str] = {
        1: "up",
        2: "right",
        3: "down",
        4: "left"
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
        2: "Multiplayer with turn limit",
        3: "Singleplayer against easy PC",
        4: "Singleplayer against easy PC with turn limit",
        5: "Singleplayer against normal PC",
        6: "Singleplayer against normal PC with turn limit"
    }
    TEXT_INDENT: int = 4


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
            print(f"{' ':<Constants.TEXT_INDENT}{key}: {value}")
        try:
            selected_mode = int(input("\nSelect game mode.\n"))
            if selected_mode < 1 or selected_mode > len(Constants.GAME_MODES):
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid number.\n")
    print(f"Selected '{Constants.GAME_MODES[selected_mode]}' mode.")
    return selected_mode


def get_turn_limit() -> int:
    """Ask user to specify game length."""
    turn_limit = 0
    while turn_limit not in range(5, 51):
        try:
            turn_limit = int(
                input("Select maximum number of turns from 5 - 50:\n"))
        except ValueError:
            print("Invalid input, type in a number 5 - 50\n")
    return turn_limit


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


def remove_ship():
    """Remove placed ship from player board."""


def get_user_coords(player_board: list[list[str]],
                    phase: str, board_size: int) -> tuple[int, int]:
    """Ask user for coordinates."""
    user_coords: str = ""
    translated: tuple[int, int] = (-1, -1)
    while (translated == (-1, -1)
           or player_board[translated[0]][translated[1]] != "O"):
        if phase == "placement":
            user_coords = input("Enter ship's frontal coordinates.\n")
        elif phase == "shooting":
            user_coords = input("Enter coordinates to fire cannons at.\n")
        normalized = normalize_coords(user_coords)
        if validate_coords(normalized, board_size, player_board) is True:
            translated = translate_coords(normalized)
            user_coords = normalized
        else:
            print("Invalid coordinates or already used.")
            continue
    return translated


def get_ship_direction():
    """Ask user for ship direction placement."""
    ship_direction = 0
    while ship_direction not in Constants.SHIP_DIRECTION:
        print("Choose ship's direction\n")
        for key, value in Constants.SHIP_DIRECTION.items():
            print(f"{' ':<Constants.TEXT_INDENT}{key}: {value}")
        try:
            ship_direction = int(input("Enter number of your choice.\n"))
            if ship_direction not in Constants.SHIP_DIRECTION:
                raise ValueError
        except ValueError:
            print(
                f"""Please input a number from\
                    1 - {len(Constants.SHIP_DIRECTION)}""")
            continue
        return (Constants.SHIP_DIRECTION[ship_direction])


def get_ship_type() -> str:
    """Ask user which ship type to place on board."""
    ship_type: str = ""
    while ship_type not in Constants.SHIP_TYPES:
        print("Ship types:")
        for name in Constants.SHIP_TYPES:
            print(f"{' ':<Constants.TEXT_INDENT} {name}")
        try:
            ship_type = input("\nSelect a type of ship.\n").lower()
            if ship_type not in Constants.SHIP_TYPES:
                raise ValueError
        except ValueError:
            print("\nUnknown ship type.\n")
    return ship_type


def validate_coords(user_coords: str, board_size: int,
                    board: list[list[str]]) -> bool:
    """Check if input coordinates are within board bounds and weren't taken."""
    check_coords: tuple[int, int] = translate_coords(user_coords)
    if check_coords[0] in range(board_size):
        if check_coords[1] in range(board_size):
            if board[check_coords[0]][check_coords[1]] == "O":
                return True
    return False


def normalize_coords(raw_coords: str) -> str:
    """Convert user input into a format used in coordinates translation."""
    move_list: list[str] = [*raw_coords]
    move_list[0] = move_list[0].upper()
    normalized_move = ''.join(move_list)
    return normalized_move


def translate_coords(raw_coords: str) -> tuple[int, int]:
    """Convert user input into a format used in the game."""
    converted: list[int] = [int(int(raw_coords[1::]) - 1),
                            int(Constants.COORDS_TRANSLATION[raw_coords[0]])]
    return converted[0], converted[1]


def get_empty_board(board_size: int) -> list[list[str]]:
    """Create new playable board."""
    board: list[list[str]] = []
    for row in range(board_size):
        board.append([])
        for _ in range(board_size):
            board[row].append("O")
    return board


def display_board(game_board: list[str], selected_size: int) -> None:
    """Display board to the user."""
    print(f'{""}\t{"A"}\t{"B"}\t{"C"}\t{"D"}\t{"E"}')
    for id_position, position in enumerate(game_board, start=1):
        print(id_position, *position, sep='\t')


def display_turns_left(turn_counter: int) -> None:
    """Display how many turns are left."""
    print(turn_counter)


def convert_board(board: list[list[str]]) -> list[str]:
    """Convert iterable board into multi line string."""
    board = board.copy()
    return [""]


def check_ship_proximity(player_board: list[list[str]],  # Function has a bug
                         converted_coords: tuple[int, int],
                         ship_type: list[str],
                         ship_direction: str) -> bool:
    """Check if ship placement attempt has enough space."""
    coords_list: list[tuple[int, int]] = ship_coords(
        converted_coords, ship_direction, ship_type)
    confirm_list: list[bool] = []
    for coords in coords_list:
        position_check: list[bool] = []
        row, col = coords
        position_check.append(player_board[row][col] == "O")
        if row == 0:
            position_check.append(
                player_board[row][col] in ["O", IndexError])
        else:
            position_check.append(
                player_board[row-1][col] in ["O", IndexError])
        if row == len(player_board)-1:
            position_check.append(
                player_board[row][col] in ["O", IndexError])
        else:
            position_check.append(
                player_board[row+1][col] in ["O", IndexError])
        if col == len(player_board[0])-1:
            position_check.append(
                player_board[row][col] in ["O", IndexError])
        else:
            position_check.append(
                player_board[row][col+1] in ["O", IndexError])
        if col == 0:
            position_check.append(
                player_board[row][col] in ["O", IndexError])
        else:
            position_check.append(
                player_board[row][col-1] in ["O", IndexError])
        confirm_list.append(all(position_check))
    if all(confirm_list) is True:
        return True
    return False


def ship_coords(coords, orientation, ship):  # fix variable names
    """Convert ship into a list of coordinates."""
    temp_ship = []
    working_coords = coords
    for _ in ship:
        temp_ship.append(working_coords)
        if orientation == "down":
            working_coords = working_coords[0]+1, working_coords[1]
        if orientation == "right":
            working_coords = working_coords[0], working_coords[1]+1
        if orientation == "up":
            working_coords = working_coords[0]-1, working_coords[1]
        if orientation == "left":
            working_coords = working_coords[0], working_coords[1]-1
    return temp_ship


def waiting_screen():
    print("""\n
    \n
    \n
    \n
 _       __        _  __     ____               __  __                       __                    
| |     / /____ _ (_)/ /_   / __/____   _____   \ \/ /____   __  __ _____   / /_ __  __ _____ ______ 
| | /| / // __ `// // __/  / /_ / __ \ / ___/    \  // __ \ / / / // ___/  / __// / / // ___// __  /
| |/ |/ // /_/ // // /_   / __// /_/ // /        / // /_/ // /_/ // /     / /_ / /_/ // /   / / / /
|__/|__/ \__,_//_/ \__/  /_/   \____//_/        /_/ \____/ \__,_//_/      \__/ \__,_//_/   /_/ /_/ 
                                                                                                    \n
                                                                                                    \n
                                                                                                    """)

    input1 = input("Press any key to continue:")
    # if input1:
    #     game_continue()
    # pass


def clear_terminal() -> None:
    """Terminal cleaning for proper animation display."""
    if operating_system() == "Windows":
        def clear():
            return system("cls")
        clear()  # on Windows systems
    else:
        system("clear")  # on Unix systems


def boards_side_by_side(player1_visible_board: list[list[str]],
                        player2_visible_board: list[list[str]],
                        board_size: int) -> str:
    """Display both players visible board versions side by side."""
    boards = convert_board(player1_visible_board), convert_board(
        player2_visible_board)
    for i in range(board_size):
        print()
        for j in range(2):
            print(boards[j][i], end=' ')
    return ""


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

# for i in range(board_size):
#

def whose_turn_is_it(turn_counter: int) -> str:
    """Get player symbol based on turn number."""
    return "Player 2" if turn_counter % 2 == 0 else "Player 1"


def check_if_sunk():
    """Confirm that a ship has been sunk."""


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
    print(hit_miss_sunk)


def check_for_winner(player_board: list[list[str]]) -> tuple[bool, int]:
    """Check if a player won after his last move."""
    player_board = player_board.copy()
    return False, 69  # Nice


def get_winner(player_board: list[list[str]],
               turn: int) -> None:
    """Display a message which player won."""
    player_board = player_board.copy()
    print(turn)


def bot_ship_placement():
    """Placement phase for bot in singleplayer."""


def easy_bot_move(game_board: list[list[str]]) -> tuple[int, int]:
    """Random choice for bot from game board."""
    row: int = -1
    col: int = -1
    while game_board[row][col] != "O":
        row, col = randint(0, len(game_board)), randint(0, len(game_board[0]))
    return row, col


def normal_bot_move():
    """Bot attempt to sink a ship."""


def settings_phase():
    """Combine functions for mode selection."""


def placement_phase():
    """Combine functions for placement phase."""


def shooting_phase():
    """Combine functions for shooting phase."""


def main() -> None:
    """Combine actual game logic."""


def attempt_feedback(hit_missed_sunk: str) -> None:
    if validate_coords() == False:
        print("Invalid input!")
    if check_ship_proximity() == False:
        print("Ships are too close!")
    if hit_missed_sunk == "X":
        print("You've hit a ship!")
    elif hit_missed_sunk == "M":
        print("You've missed!")
    elif hit_missed_sunk == "S":
        print("You've sunk a ship!")


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
