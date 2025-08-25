import os

# Main file for our chess application.
# This will contain the game logic.

def create_board():
    """
    Creates a new chess board with pieces in their starting positions.
    Uses a 2D list (8x8) to represent the board.
    Uppercase letters are white pieces, lowercase are black pieces.
    ' ' represents an empty square.
    """
    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    return board

def print_board(board):
    """
    Prints the given chess board to the console.
    """
    print("  a b c d e f g h")
    print(" +-----------------+")
    for i, row in enumerate(board):
        print(f"{8 - i}| {' '.join(row)} |{8 - i}")
    print(" +-----------------+")
    print("  a b c d e f g h")

def parse_move(move_str):
    """
    Parses a move string in algebraic notation (e.g., 'e2e4')
    and returns the start and end positions as tuples of (row, col).
    """
    if len(move_str) != 4:
        raise ValueError("Move string must be 4 characters long (e.g., 'e2e4').")

    start_col_char = move_str[0]
    start_row_char = move_str[1]
    end_col_char = move_str[2]
    end_row_char = move_str[3]

    # Convert file (column) character to index (0-7)
    col_map = {chr(ord('a') + i): i for i in range(8)}
    if start_col_char not in col_map or end_col_char not in col_map:
        raise ValueError("Invalid column character. Use 'a' through 'h'.")
    start_col = col_map[start_col_char]
    end_col = col_map[end_col_char]

    # Convert rank (row) character to index (0-7)
    if not start_row_char.isdigit() or not end_row_char.isdigit():
        raise ValueError("Invalid row character. Use '1' through '8'.")
    start_row = 8 - int(start_row_char)
    end_row = 8 - int(end_row_char)

    if not (0 <= start_row <= 7 and 0 <= end_row <= 7):
        raise ValueError("Row is out of bounds. Use '1' through '8'.")

    return (start_row, start_col), (end_row, end_col)

def make_move(board, start_pos, end_pos, turn):
    """
    Moves a piece on the board from start_pos to end_pos.
    Validates that the player is moving their own piece.
    """
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = board[start_row][start_col]
    if piece == ' ':
        raise ValueError("The starting square is empty.")

    # Check if the piece color matches the current turn
    is_white_piece = piece.isupper()
    if turn == 'white' and not is_white_piece:
        raise ValueError("It is White's turn, but you tried to move a Black piece.")
    if turn == 'black' and is_white_piece:
        raise ValueError("It is Black's turn, but you tried to move a White piece.")

    board[end_row][end_col] = piece
    board[start_row][start_col] = ' '
    return board

if __name__ == '__main__':
    game_board = create_board()
    turn = 'white'

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("A new game of chess has started!")
        print_board(game_board)

        prompt = f"{turn.capitalize()}'s move (e.g., e2e4) or 'exit' to quit: "
        move_str = input(prompt)

        if move_str.lower() == 'exit':
            print("Thanks for playing!")
            break

        try:
            start_pos, end_pos = parse_move(move_str)
            game_board = make_move(game_board, start_pos, end_pos, turn)

            # Switch turns
            if turn == 'white':
                turn = 'black'
            else:
                turn = 'white'

        except ValueError as e:
            print(f"\nError: {e}")
            input("Press Enter to continue...")
