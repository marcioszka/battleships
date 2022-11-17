"""A game of battleships."""

from os import system
from platform import system as operating_system
from random import randint
from string import ascii_uppercase
from time import sleep


class Globals:  # pylint: disable=[too-few-public-methods]
    """Globally accessed variables."""

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
    # pylint: disable=[line-too-long]
    WAITING_MESSAGE = [
        " _       __        _  __     ____               __  __                       __",
        "| |     / /____ _ (_)/ /_   / __/____   _____   \\ \\/ /____   __  __ _____   / /_ __  __ _____ ______",
        "| | /| / // __ `// // __/  / /_ / __ \\ / ___/    \\  // __ \\ / / / // ___/  / __// / / // ___// __  /",
        "| |/ |/ // /_/ // // /_   / __// /_/ // /        / // /_/ // /_/ // /     / /_ / /_/ // /   / / / /",
        "|__/|__/ \\__,_//_/ \\__/  /_/   \\____//_/        /_/ \\____/ \\__,_//_/      \\__/ \\__,_//_/   /_/ /_/"

    ]
    # pylint: enable=[line-too-long]
    PLAYER1_SHIPS: dict[str, list[tuple[int, int]]] = {}
    PLAYER2_SHIPS: dict[str, list[tuple[int, int]]] = {}
    PLAYER1_HITS: dict[str, list[tuple[int, int]]] = {}
    PLAYER2_HITS: dict[str, list[tuple[int, int]]] = {}


def generate_board_size(selected_size: int) -> None:
    """Populate game constants with size adjusted values."""
    Globals.COORDS_TRANSLATION = dict(
        zip(ascii_uppercase[:selected_size], range(selected_size)))
    Globals.VALID_COORDINATES = [row+str(column) for column in
                                 range(selected_size)
                                 for row in Globals.COORDS_TRANSLATION]


def get_game_mode() -> int:
    """Ask user to select a game mode."""
    selected_mode = 0
    print("Available modes:")
    while selected_mode not in Globals.GAME_MODES:
        for key, value in Globals.GAME_MODES.items():
            print(f"{' ':<Globals.TEXT_INDENT}{key}: {value}")
        try:
            selected_mode = int(input("\nSelect game mode.\n"))
            if selected_mode < 1 or selected_mode > len(Globals.GAME_MODES):
                raise ValueError
        except ValueError:
            print("\nPlease enter a valid number.\n")
    print(f"Selected '{Globals.GAME_MODES[selected_mode]}' mode.")
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
    while ship_direction not in Globals.SHIP_DIRECTION:
        print("Choose ship's direction\n")
        for key, value in Globals.SHIP_DIRECTION.items():
            print(f"{' ':<Globals.TEXT_INDENT}{key}: {value}")
        try:
            ship_direction = int(input("Enter number of your choice.\n"))
            if ship_direction not in Globals.SHIP_DIRECTION:
                raise ValueError
        except ValueError:
            print(
                f"""Please input a number from\
                    1 - {len(Globals.SHIP_DIRECTION)}""")
            continue
        return Globals.SHIP_DIRECTION[ship_direction]


def get_ship_type() -> str:
    """Ask user which ship type to place on board."""
    ship_type: str = ""
    while ship_type not in Globals.SHIP_TYPES:
        print("Ship types:")
        for name in Globals.SHIP_TYPES:
            print(f"{' ':<Globals.TEXT_INDENT} {name}")
        try:
            ship_type = input("\nSelect a type of ship.\n").lower()
            if ship_type not in Globals.SHIP_TYPES:
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
                            int(Globals.COORDS_TRANSLATION[raw_coords[0]])]
    return converted[0], converted[1]


def get_empty_board(board_size: int) -> list[list[str]]:
    """Create new playable board."""
    board: list[list[str]] = []
    for row in range(board_size):
        board.append([])
        for _ in range(board_size):
            board[row].append("O")
    return board


def display_board(game_board: list[list[str]]) -> None:
    """Display board to the user."""
    print(" ", end="\t")
    for key in Globals.COORDS_TRANSLATION:
        print(key, end="\t")
    print("\n")
    for id_position, position in enumerate(game_board, start=1):
        print(f"{str(id_position):>2}", *position, sep='\t')


def display_turns_left(turn_counter: int) -> None:
    """Display how many turns are left."""
    print(f"{'':>Globals.TEXT_INDENT}Turns left: {turn_counter}")


def convert_board(board: list[list[str]]) -> list[str]:
    """Convert iterable board into multi line string."""
    column_names = []
    column_names.append("\t")
    for letter in Globals.COORDS_TRANSLATION:
        column_names.append((letter + " "))
    column_names = [''.join(column_names)]
    board_body = []
    for id_position, position in enumerate(board, start=1):
        row = []
        row.append((str(id_position) + "\t"))
        row.append((' '.join([*position])))
        board_body.append(''.join(row))
    stringified_board = column_names + board_body
    return stringified_board


def check_ship_proximity(player_board: list[list[str]],
                         converted_coords: tuple[int, int],
                         ship_type: str,
                         ship_direction: str) -> bool:
    """Check if ship placement attempt has enough space."""
    coords_list: list[tuple[int, int]] = extend_ship(
        converted_coords, ship_direction, ship_type)
    confirm_list: list[bool] = []
    for coordinate in coords_list:
        position_check: list[bool] = []
        row, col = coordinate
        position_check.append(player_board[row][col] == "O")
        if row == 0:
            position_check.append(
                player_board[row][col] == "O")
        else:
            position_check.append(
                player_board[row-1][col] == "O")
        if col == 0:
            position_check.append(
                player_board[row][col] == "O")
        else:
            position_check.append(
                player_board[row][col-1] == "O")
        try:
            position_check.append(
                player_board[row+1][col] == "O")
            position_check.append(
                player_board[row][col+1] == "O")
        except IndexError:
            position_check.append(
                player_board[row][col] == "O")
        confirm_list.append(all(position_check))
    if all(confirm_list) is True:
        return True
    return False


def extend_ship(front_position: tuple[int, int],
                orientation: str, ship: str) -> list[tuple[int, int]]:
    """Convert ship into a list of coordinates."""
    temp_ship = []
    ship_element = front_position
    for _ in Globals.SHIP_TYPES[ship]:
        temp_ship.append(ship_element)
        try:
            if orientation == "up":
                if ship_element[0] == 0:
                    raise IndexError
                ship_element = ship_element[0]-1, ship_element[1]
            if orientation == "left":
                if ship_element[1] == 0:
                    raise IndexError
                ship_element = ship_element[0], ship_element[1]-1
            if orientation == "down":
                ship_element = ship_element[0]+1, ship_element[1]
            if orientation == "right":
                ship_element = ship_element[0], ship_element[1]+1
        except IndexError:
            print("Ship out of bounds!")
    return temp_ship


def waiting_screen():
    """Print waiting message for player swap."""
    clear_terminal()
    print("\n\n\n")
    for line in Globals.WAITING_MESSAGE:
        print(line)
    print("\n\n\n")
    input("Press any key to continue.")
    clear_terminal()


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
                        board_size: int) -> None:
    """Display both players visible board versions side by side."""
    boards = convert_board(player1_visible_board), convert_board(
        player2_visible_board)
    print(boards[0][0], end='')
    print("\t", end='')
    print(boards[1][0], end='')
    print("\n")
    for i in range(1, board_size+1):
        for j in range(2):
            print(boards[j][i], end='')
            print("\t", end='')
        print()


def whose_turn_is_it(turn_counter: int) -> str:
    """Get player symbol based on turn number."""
    return "Player 2" if turn_counter % 2 == 0 else "Player 1"


def check_if_sunk(turn_counter: int, attack_coords: tuple[int, int]) -> bool:
    """Confirm that a ship has been sunk."""
    enemy_ships: dict[str, list[tuple[int, int]]] = {}
    hit_ship: str = ""
    if whose_turn_is_it(turn_counter) == "Player 1":
        enemy_ships = Globals.PLAYER2_SHIPS
        for ship, coords in enemy_ships.items():
            if attack_coords in coords:
                hit_ship = ship
    if whose_turn_is_it(turn_counter) == "Player 2":
        enemy_ships = Globals.PLAYER1_SHIPS
        for ship, coords in enemy_ships.items():
            if attack_coords in coords:
                hit_ship = ship
    if len(enemy_ships[hit_ship]) < 1:
        return True
    return False


def place_move_on_board(defender_visible_board: list[list[str]],
                        turn_counter: int,
                        attack_coords: tuple[int, int],
                        ship_name: str,
                        ship_direction: str) -> list[list[str]]:
    """Place attack coordinates result on player boards."""
    row, col = attack_coords
    board = defender_visible_board
    if board[row][col] == "O":
        if whose_turn_is_it(turn_counter) == "Player 1":
            if attack_coords in Globals.PLAYER2_SHIPS.values():
                board[row][col] = "H"
                Globals.PLAYER2_SHIPS[ship_name].remove(attack_coords)
                if Globals.PLAYER1_HITS[ship_name]:
                    Globals.PLAYER1_HITS[ship_name].append(attack_coords)
                else:
                    Globals.PLAYER1_HITS.update({ship_name: [attack_coords]})
            else:
                board[row][col] = "M"
        if whose_turn_is_it(turn_counter) == "Player 2":
            if attack_coords in Globals.PLAYER1_SHIPS.values():
                board[row][col] = "H"
                Globals.PLAYER1_SHIPS[ship_name].remove(attack_coords)
                if Globals.PLAYER2_HITS[ship_name]:
                    Globals.PLAYER2_HITS[ship_name].append(attack_coords)
                else:
                    Globals.PLAYER2_HITS.update({ship_name: [attack_coords]})
            else:
                board[row][col] = "M"
    if check_if_sunk(turn_counter, attack_coords):
        if whose_turn_is_it(turn_counter) == "Player 1":
            for ship_element in Globals.PLAYER1_HITS[ship_name]:
                board[ship_element[0]][ship_element[1]] = "S"
        if whose_turn_is_it(turn_counter) == "Player 2":
            for ship_element in Globals.PLAYER2_HITS[ship_name]:
                board[ship_element[0]][ship_element[1]] = "S"
        attempt_feedback(turn_counter, attack_coords,
                         board, ship_name, ship_direction)
    return board


def attempt_feedback(turn_counter: int,
                     attack_coords: tuple[int, int],
                     player_board: list[list[str]],
                     ship_name: str,
                     ship_direction: str
                     ) -> None:
    """User feedback based on his move attempt."""
    if check_ship_proximity(player_board, attack_coords,
                            ship_name, ship_direction) is False:
        print("Ships are too close!")
    if player_board[attack_coords[0]][attack_coords[1]] == "X":
        print("You've hit a ship!")
    elif player_board[attack_coords[0]][attack_coords[1]] == "M":
        print("You've missed!")
    elif player_board[attack_coords[0]][attack_coords[1]] == "S":
        print(f"{whose_turn_is_it(turn_counter)} {ship_name} has been sunk!")


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


if __name__ == "__main__":
    # Testing and execution purpose

    # main()
    # get_ship_type()
    # print(COORDS_TRANSLATION)
    # print(translate_coords("J2138"))
    # get_game_mode()
    # print(Globals.COORDS_TRANSLATION)
    # print(Globals.VALID_COORDINATES)
    # get_board_size()
    # print(Globals.VALID_COORDINATES)
    # print(Globals.COORDS_TRANSLATION)
    print(get_empty_board(10))
