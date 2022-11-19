"""A game of battleships."""
from copy import deepcopy
from time import sleep
from string import ascii_uppercase
from random import choice, randint
from platform import system as operating_system
from os import system


# global JAKAS_ZMIENNA = ""

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
        5: "Singleplayer against normal PC (not implemented)",
        6: "Singleplayer against normal PC with turn limit (not implemented)"
    }
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
    P1_SHIPS_FOR_P2: dict[str, list[tuple[int, int]]] = {}
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
            print(f"    {key}: {value}")
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
    generate_board_size(selected_size)
    print("Generating board", end="", flush=True)
    sleep(0.5)
    print(".", end="", flush=True)
    sleep(0.5)
    print(".", end="", flush=True)
    sleep(0.5)
    print(".\n", flush=True)
    sleep(0.5)
    print(f"Board with size {selected_size} generated.\n\n")
    return selected_size


def confirm_placement(player_board: list[list[str]],
                      converted_coords: tuple[int, int],
                      ship_type: str,
                      ship_direction: str,
                      turn_counter: int) -> list[list[str]]:
    """Ask user for confirmation of ship placement."""
    player_decision: str = ""
    decisions: list[str] = ["yes", "no"]
    player_ships: dict[str, list[tuple[int, int]]] = {}
    active_board: list[list[str]] = deepcopy(player_board)
    if turn_counter % 2 == 0:
        player_ships = Globals.P1_SHIPS_FOR_P2
    else:
        player_ships = Globals.PLAYER1_SHIPS
    temp_board = place_ship(player_board, converted_coords,
                            ship_type, ship_direction, turn_counter)
    if temp_board == active_board:
        return player_board
    while player_decision not in decisions:
        display_board(temp_board)
        player_decision = input(
            "Do You accept such ship placement?\nenter:yes/no\n")
        if player_decision == "yes":
            print("ship placement was accepted\n")
            return temp_board
        if player_decision == "no":
            print("ship placement was not accepted\n")
            if turn_counter % 2 == 0:
                pass
            else:
                player_ships.pop(ship_type)
        else:
            print('invalid input, please enter "Yes" or "No"')
    return player_board


def remove_ship(turn_counter: int,
                player_board: list[list[str]]) -> list[list[str]]:
    """Remove placed ship from player board."""
    ships_position: list[list[tuple[int, int]]] = []
    ships_on_board: list[str] = []
    if turn_counter % 2 == 0:
        for ship_name, ship_position in Globals.PLAYER2_SHIPS.items():
            ships_position.append(ship_position)
            ships_on_board.append(ship_name)
    else:
        for ship_name, ship_position in Globals.PLAYER1_SHIPS.items():
            ships_position.append(ship_position)
            ships_on_board.append(ship_name)
    print("You've placed following ships on your board:")
    for ship in ships_on_board:
        i = 1
        print(f"{i}. {ship:>2} starting at", end="")
        print(f"{ships_position[ships_on_board.index(ship)][0]}")
        i += 1
    ship_to_remove: str = input("Which one would you like to remove?\n")
    if ship_to_remove not in ships_on_board:
        return player_board
    ship_index = ships_on_board.index(ship_to_remove)
    for row, col in ships_position[ship_index]:
        player_board[row][col] = 'O'
    ships_position.pop(ship_index)
    ships_on_board.pop(ship_index)
    if turn_counter % 2 == 0:
        Globals.PLAYER2_SHIPS.pop(ship_to_remove)
    else:
        Globals.PLAYER1_SHIPS.pop(ship_to_remove)
    return player_board


def get_user_coords(player_board: list[list[str]],
                    phase: str, board_size: int) -> tuple[int, int]:
    """Ask user for coordinates."""
    user_coords: str = ""
    translated: tuple[int, int] = (-1, -1)
    normalized: str = ""
    while (translated == (-1, -1)
           or player_board[translated[0]][translated[1]] != "O"):
        if phase == "placement":
            user_coords = input("Enter ship's frontal coordinates.\n")
        elif phase == "shooting":
            user_coords = input("Enter coordinates to fire cannons at.\n")
        try:
            if user_coords[0].upper() not in Globals.COORDS_TRANSLATION:
                raise ValueError
            if (isinstance(user_coords[0], str)
                    and isinstance(int(user_coords[1]), int)):
                normalized = normalize_coords(user_coords)
        except ValueError:
            print("Invalid coordinates or already used.")
            continue
        if validate_coords(normalized, board_size, player_board) is True:
            translated = translate_coords(normalized)
            user_coords = normalized
        else:
            print("Invalid coordinates or already used.")
            continue
    return translated


def get_ship_direction() -> str:
    """Ask user for ship direction placement."""
    ship_direction = 0
    while ship_direction not in Globals.SHIP_DIRECTION:
        print("Choose ship's direction")
        for key, value in Globals.SHIP_DIRECTION.items():
            print(f"    {key}: {value}")
        try:
            ship_direction = int(input("Enter number of your choice.\n"))
            if ship_direction not in Globals.SHIP_DIRECTION:
                raise ValueError
        except ValueError:
            print("Please input a number from", end="")
            print(f"1 - {len(Globals.SHIP_DIRECTION)}")
            continue
    return Globals.SHIP_DIRECTION[ship_direction]


def get_ship_type(player: int) -> str:
    """Ask user which ship type to place on board."""
    ship_type: str = ""
    names: list[str] = []
    ship_length: list[list[tuple[int, int]]] = []
    index: int = 0
    if player == 2:
        for ship, coords in Globals.P1_SHIPS_FOR_P2.items():
            names.append(ship)
            ship_length.append([])
            for coord in coords:
                ship_length[index].append(coord)
            index += 1
        index = 0
    while (player == 1 and ship_type not in Globals.SHIP_TYPES
           or (player == 2 and ship_type not in names)):
        print("Ship types:")
        if player == 1:
            for name, length in Globals.SHIP_TYPES.items():
                print(f"    {name.capitalize()}", end="")
                print(f" - size: {len(length)}")
        else:
            for name in names:
                print(f"    {name.capitalize()}", end="")
                print(f" - size: {len(ship_length[index])}")
                index += 1
            index = 0
        try:
            ship_type = input("\nSelect a type of ship.\n").lower()
            if (player == 1 and ship_type not in Globals.SHIP_TYPES
                    or (player == 2 and ship_type not in names)):
                raise ValueError
        except ValueError:
            print("\nUnknown ship type.\n")
    if player == 2:
        index = names.index(ship_type)
        names.pop(index)
        ship_length.pop(index)
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
    normalized_move: list[str] = []
    normalized_move.append(move_list[0].upper())
    normalized_move.append(move_list[1])
    normalized = ''.join(normalized_move)
    return normalized


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
    board = convert_board(game_board)
    print("\n\n")
    print(board[0])
    print()
    for i in range(1, len(game_board)+1):
        print(board[i])
    print("\n\n")


def display_turns_left(turn_counter: int) -> None:
    """Display how many turns are left."""
    print(f"    Turns left: {turn_counter}")


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


def place_ship(player_board: list[list[str]],
               converted_coords: tuple[int, int],
               ship_type: str,
               ship_direction: str,
               turn_counter: int) -> list[list[str]]:
    """Placement of selected ship on board"""
    coords_list: list[tuple[int, int]] = extend_ship(
        converted_coords, turn_counter % 2, ship_direction, ship_type)
    if len(coords_list) > 1:
        for row, col in coords_list:
            if (row >= len(player_board) or col >= len(player_board)
                    or row < 0 or col < 0):
                print("Ship out of bounds!")
                coords_list = []
                return player_board
    else:
        coords_list = [converted_coords]
    if check_ship_proximity(player_board, coords_list):
        for row, col in coords_list:
            player_board[row][col] = "X"
        if whose_turn_is_it(turn_counter) == "Player 1":
            if Globals.PLAYER1_SHIPS.get(ship_type) is not None:
                ship_name: str = ship_type
                counter = 1
                new_name: str = str(ship_name + str(counter))
                while isinstance(Globals.PLAYER1_SHIPS
                                 .get(str(new_name)), list):
                    counter += 1
                    new_name = str(ship_name + str(counter))
                ship_name = new_name
                Globals.PLAYER1_SHIPS.update({ship_name: coords_list})
                Globals.P1_SHIPS_FOR_P2.update({ship_name: coords_list})
            else:
                Globals.PLAYER1_SHIPS.update({ship_type: coords_list})
                Globals.P1_SHIPS_FOR_P2.update({ship_type: coords_list})
        if whose_turn_is_it(turn_counter) == "Player 2":
            if Globals.PLAYER2_SHIPS.get(ship_type) is not None:
                ship_name = ship_type
                counter = 1
                new_name = str(ship_name + str(counter))
                while isinstance(Globals.PLAYER1_SHIPS
                                 .get(str(new_name)), list):
                    counter += 1
                    new_name = str(ship_name + str(counter))
                ship_name = new_name
                Globals.PLAYER2_SHIPS.update({ship_name: coords_list})
                Globals.P1_SHIPS_FOR_P2.pop(ship_name)
            else:
                Globals.PLAYER2_SHIPS.update({ship_type: coords_list})
                Globals.P1_SHIPS_FOR_P2.pop(ship_type)
        return player_board
    return player_board


def check_ship_proximity(player_board: list[list[str]],
                         coords_list: list[tuple[int, int]]) -> bool:
    """Check if ship placement attempt has enough space."""
    confirm_list: list[bool] = []
    if len(coords_list) < 1:
        print("Ship out of bounds!")
        return False
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
    print("Ship too close!")
    return False


def extend_ship(front_position: tuple[int, int], player: int,
                orientation: str, ship: str) -> list[tuple[int, int]]:
    """Convert ship into a list of coordinates."""
    temp_ship = []
    ship_element = front_position
    ships2: dict[str, list[tuple[int, int]]] = Globals.P1_SHIPS_FOR_P2
    ships1: dict[str, list[str]] = Globals.SHIP_TYPES
    if player == 1:
        for _ in ships1[ship]:
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
                temp_ship = []
    else:
        for _ in ships2[ship]:
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
                temp_ship = []
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
    print()
    for i in range(1, board_size+1):
        for j in range(2):
            print(boards[j][i], end='')
            print("\t", end='')
        print()
    print("\n\n")


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
                        attack_coords: tuple[int, int]) -> list[list[str]]:
    """Place attack coordinates result on player boards."""
    row, col = attack_coords
    board: list[list[str]] = defender_visible_board
    ship_name: str = ""
    if turn_counter % 2 == 0:
        for ship, coords in Globals.PLAYER1_SHIPS.items():
            for coord in coords:
                if coord == attack_coords:
                    ship_name = ship
    if turn_counter % 2 != 0:
        for ship, coords in Globals.PLAYER2_SHIPS.items():
            for coord in coords:
                if coord == attack_coords:
                    ship_name = ship
    if board[row][col] == "O":
        if whose_turn_is_it(turn_counter) == "Player 1":
            if attack_coords in Globals.PLAYER2_SHIPS[ship_name]:
                board[row][col] = "H"
                attempt_feedback(turn_counter, attack_coords,
                                 board, ship_name)
                Globals.PLAYER2_SHIPS[ship_name].remove(attack_coords)
                if isinstance(Globals.PLAYER1_HITS.get(ship_name), list):
                    Globals.PLAYER1_HITS[ship_name].append(attack_coords)
                else:
                    Globals.PLAYER1_HITS.update({ship_name: [attack_coords]})
            else:
                board[row][col] = "M"
                attempt_feedback(turn_counter, attack_coords,
                                 board, ship_name)
        if whose_turn_is_it(turn_counter) == "Player 2":
            if attack_coords in Globals.PLAYER1_SHIPS[ship_name]:
                board[row][col] = "H"
                attempt_feedback(turn_counter, attack_coords,
                                 board, ship_name)
                Globals.PLAYER1_SHIPS[ship_name].remove(attack_coords)
                if isinstance(Globals.PLAYER2_HITS.get(ship_name), list):
                    Globals.PLAYER2_HITS[ship_name].append(attack_coords)
                else:
                    Globals.PLAYER2_HITS.update({ship_name: [attack_coords]})
            else:
                board[row][col] = "M"
                attempt_feedback(turn_counter, attack_coords,
                                 board, ship_name)
    if check_if_sunk(turn_counter, attack_coords):
        if whose_turn_is_it(turn_counter) == "Player 1":
            for ship_element in Globals.PLAYER1_HITS[ship_name]:
                board[ship_element[0]][ship_element[1]] = "S"
        if whose_turn_is_it(turn_counter) == "Player 2":
            for ship_element in Globals.PLAYER2_HITS[ship_name]:
                board[ship_element[0]][ship_element[1]] = "S"
        attempt_feedback(turn_counter, attack_coords,
                         board, ship_name)
    return board


def attempt_feedback(turn_counter: int,
                     attack_coords: tuple[int, int],
                     player_board: list[list[str]],
                     ship_name: str) -> None:
    """User feedback based on his move attempt."""
    row, col = attack_coords
    if player_board[row][col] == "X":
        print("You've hit a ship!")
    elif player_board[row][col] == "M":
        print("You've missed!")
    elif player_board[row][col] == "S":
        print(f"{whose_turn_is_it(turn_counter)} {ship_name} has been sunk!")


def check_for_winner(turn_counter: int) -> str:
    """Check if a player won after his last move."""
    winner = ""
    if turn_counter % 2 == 0 and len(Globals.PLAYER1_SHIPS) == 0:
        winner = "Player 2"
    elif turn_counter % 2 != 0 and len(Globals.PLAYER2_SHIPS) == 0:
        winner = "Player 1"
    return winner


def get_winner(winner: str) -> None:
    """Display a message which player won."""
    print(f'{winner} has won!\nSuch a smartie!')


def bot_ship_placement(bot_board: list[list[str]]) -> list[list[str]]:
    """Placement phase for bot in singleplayer."""
    ships_to_place: list[str] = []
    directions: list[str] = []
    for ship in Globals.PLAYER1_SHIPS:
        ships_to_place.append(
            ''.join(letter for letter in ship if letter.isdigit() is False))
    for direction in Globals.SHIP_DIRECTION.values():
        directions.append(direction)
    while len(ships_to_place) != 0:
        ships: list[str] = []
        for ship in ships_to_place:
            ships.append(ship)
        selected_ship: str = choice(ships)
        ship_direction: str = choice(directions)
        placement_coords: tuple[int, int] = easy_bot_move(bot_board)
        coords_list: list[tuple[int, int]] = extend_ship(
            placement_coords, 2, ship_direction, selected_ship)
        if check_ship_proximity(bot_board, coords_list):
            place_ship(
                bot_board, placement_coords, selected_ship, ship_direction, 2)
    return bot_board


def easy_bot_move(game_board: list[list[str]]) -> tuple[int, int]:
    """Random choice for bot from game board."""
    row: int = randint(0, len(game_board[0])-1)
    col: int = randint(0, len(game_board[0])-1)
    while game_board[row][col] != "O":
        row, col = randint(0, len(game_board)), randint(0, len(game_board[0]))
    return row, col


def normal_bot_move():
    """Bot attempt to sink a ship."""


def settings_phase() -> list[int]:
    """Combine functions for mode selection."""
    game_mode: int = 0
    turn_limit: int = 0
    while game_mode == 0:
        game_mode = get_game_mode()
        if game_mode in [5, 6]:
            print("Game mode not implemented, starting as easy PC")
            game_mode -= 2
        if game_mode in [2, 4]:
            turn_limit = get_turn_limit()
    board_size: int = get_board_size()
    return [game_mode, turn_limit, board_size]


def placement_phase(game_mode: int, board_size: int
                    ) -> None:
    """Combine functions for placement phase."""
    p1_board: list[list[str]] = get_empty_board(board_size)
    p2_board: list[list[str]] = get_empty_board(board_size)
    active_board: list[list[str]] = []
    end: bool = False
    selection: int = 0
    player: int = 1
    while end is False or (player == 2 and game_mode not in range(3, 7)):
        if player == 1:
            ships: dict[str, list[tuple[int, int]]] = Globals.PLAYER1_SHIPS
            active_board = p1_board
        else:
            ships = Globals.PLAYER2_SHIPS
            active_board = p2_board
        print("Select an option index from the list below.\n")
        print("1. Place ship\n")
        if len(ships) == 0:
            print("More options become visible after placing ships.\n")
        if len(ships) > 0:
            print("2. Remove ship\n")
        if len(ships) == len(Globals.PLAYER1_SHIPS) and player == 2:
            print("3. Start game\n")
        if len(ships) > 1 and player == 1:
            print("3. Pass placement to 2nd player\n")
        while selection < 1 or selection > 3:
            try:
                selection = int(input("Select option:  "))
                if selection < 1 or selection > 3:
                    raise ValueError
            except ValueError:
                print("Invalid option")
        if (selection == 1 or (selection == 1 and player == 2
                               and Globals.PLAYER2_SHIPS
                               != Globals.PLAYER1_SHIPS)):
            display_board(active_board)
            ship_type: str = get_ship_type(player)
            coords: tuple[int, int] = get_user_coords(
                active_board, "placement", board_size)
            if ship_type == "speedboat":
                direction: str = "up"
            else:
                direction = get_ship_direction()
            if player == 1:
                p1_board = confirm_placement(
                    p1_board, coords, ship_type, direction, player)
            else:
                p2_board = confirm_placement(
                    p2_board, coords, ship_type, direction, player)
        if selection == 2 and len(ships) > 0:
            remove_ship(player, active_board)
            clear_terminal()
        if (selection == 3 and player == 1 and len(ships) > 1):
            if game_mode in range(3, 7):
                break
            waiting_screen()
            player += 1
        elif (selection == 3 and player == 2
              and len(ships) == len(Globals.PLAYER1_SHIPS)):
            break
        selection = 0
    if game_mode in range(3, 7):
        bot_ship_placement(p2_board)


def shooting_phase(game_mode: int, turn_limit: int, board_size: int) -> None:
    """Combine functions for shooting phase."""
    p1_defence_board: list[list[str]] = get_empty_board(board_size)
    p2_defence_board: list[list[str]] = get_empty_board(board_size)
    turn = 1
    active_board: list[list[str]] = []
    clear_terminal()
    while True:
        if whose_turn_is_it(turn) == "Player 1":
            active_board = p2_defence_board
            print(f"It's {whose_turn_is_it(turn)} turn!\n\n")
        else:
            active_board = p1_defence_board
            print(f"It's {whose_turn_is_it(turn)} turn!\n\n")
        if game_mode in [2, 4, 6]:
            print(f"Turns left: {turn_limit - int(turn/2)}\n")
            if turn == turn_limit * 2:
                print("No more turns, it's a draw!")
                return
        boards_side_by_side(p1_defence_board, p2_defence_board, board_size)
        if game_mode in range(3, 7) and whose_turn_is_it(turn) == "Player 2":
            print(f"It's {whose_turn_is_it(turn)} turn!\n\n")
            boards_side_by_side(p1_defence_board, p2_defence_board, board_size)
        if game_mode in [1, 2] or (game_mode in range(3, 7)
                                   and whose_turn_is_it(turn) == "Player 1"):
            attack_coords: tuple[int, int] = get_user_coords(
                active_board, "shooting", board_size)
            place_move_on_board(active_board, turn, attack_coords)
        turn += 1
        if len(Globals.PLAYER1_SHIPS) == 0 or len(Globals.PLAYER2_SHIPS) == 0:
            get_winner(check_for_winner(turn))
            break


def main() -> None:
    """Combine actual game logic."""
    game_mode, turn_limit, board_size = settings_phase()
    placement_phase(game_mode, board_size)
    shooting_phase(game_mode, turn_limit, board_size)


if __name__ == "__main__":
    main()
