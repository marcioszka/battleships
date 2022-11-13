from os import system
from platform import system as operating_system

ships = {
    "battleship": ["X", "X", "X", "X", "X"],
    "miner": ["X", "X", "X", "X"],
    "ubot": ["X", "X", "X"]
}
coords_translation = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4,
    "1": 0, "2": 1, "3": 2, "4": 3, "5": 4
}
valid_coordinates = ["A1", "A2", "A3", "A4", "A5",
                     "B1", "B2", "B3", "B4", "B5",
                     "C1", "C2", "C3", "C4", "C5",
                     "D1", "D2", "D3", "D4", "D5",
                     "E1", "E2", "E3", "E4", "E5"
                     ]
type_of_field = {
    "empty": "O",
    "ship": "X",
    "missed": "M",
    "hit": "H",
    "sunk": "S"
}

# game_board = [["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"],
#               ["0", "0", "0", "0", "0"]]


def get_user_coords() -> str:
    user_coords = input("Enter ship coordinates: \n")
    return user_coords

def get_ship_direction() -> str:
    pass


def get_ship_type(ships: dict[str, list[str]]) -> str:
    pass


def validate_coords(valid_coordinates: list[str], user_coords: str) -> bool: 
    if user_coords in valid_coordinates:
        return True
    else:
        return False


def normalize_coords(user_coords: str) -> str:
    pass


def translate_coords(user_coords: str) -> tuple[int, int]:
    pass


def get_empty_board(board_size: int) -> list[str]:
    pass


def display_board(game_board: list[str]) -> None: #ja
    board_size = len(game_board)
    row = 0
    column = 0
    print(f'{"": <0}\t{"A": <0}\t{"B": <0}\t{"C": <0}\t{"D": <0}\t{"E": <0}')
    while row < board_size:
        print(f'{row+1: <0}\t{game_board[row][column]: <0}\t{game_board[row][column+1]: <0}\t{game_board[row][column+2]: <0}\t{game_board[row][column+3]: <0}\t{game_board[row][column+4]: <0}')
        row += 1


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


def boards_side_by_side(player_1_displayed_board: list[list[str]], player_2_displayed_board: list[list[str]], board_size: int) -> None: #ja
    
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


def attempt_feedback(hit_missed_sunk: str) -> None:
    
    if hit_missed_sunk == "X":
        print("You've hit a ship!")
    elif hit_missed_sunk == "M":
        print("You've missed!")
    elif hit_missed_sunk == "S":
        print("You've sunk a ship!")


def get_winner(game_board: list[str]) -> None: #ja
    pass

def display_message() -> None:
    if validate_coords() == False:
        print("Invalid input!")
    if check_ship_proximity() == False:
        print("Ships are too close!")