import copy

# This file contains the core chess game logic.

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
    Returns a new board object with the move made.
    """
    new_board = copy.deepcopy(board)
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = new_board[start_row][start_col]
    if piece == ' ':
        raise ValueError("The starting square is empty.")

    # Check if the piece color matches the current turn
    is_white_piece = piece.isupper()
    if turn == 'white' and not is_white_piece:
        raise ValueError("It is White's turn, but you tried to move a Black piece.")
    if turn == 'black' and is_white_piece:
        raise ValueError("It is Black's turn, but you tried to move a White piece.")

    # Validate the move according to chess rules
    if not is_move_valid(new_board, start_pos, end_pos):
        raise ValueError("Illegal move according to chess rules.")

    new_board[end_row][end_col] = piece
    new_board[start_row][start_col] = ' '
    return new_board

def is_move_valid(board, start_pos, end_pos):
    """
    Checks if a move is valid according to the rules of chess.
    This is the main validation function.
    """
    start_row, start_col = start_pos
    piece_char = board[start_row][start_col]
    piece_type = piece_char.lower()

    # A piece cannot move to a square occupied by a friendly piece.
    end_piece = board[end_pos[0]][end_pos[1]]
    if end_piece != ' ':
        if piece_char.isupper() == end_piece.isupper():
            return False

    if piece_type == 'p':
        return is_pawn_move_valid(board, start_pos, end_pos)
    elif piece_type == 'r':
        return is_rook_move_valid(board, start_pos, end_pos)
    elif piece_type == 'n':
        return is_knight_move_valid(board, start_pos, end_pos)
    elif piece_type == 'b':
        return is_bishop_move_valid(board, start_pos, end_pos)
    elif piece_type == 'q':
        return is_queen_move_valid(board, start_pos, end_pos)
    elif piece_type == 'k':
        return is_king_move_valid(board, start_pos, end_pos)

    return False # Should not be reached if all pieces are handled

# --- Piece-specific helper functions ---

def is_pawn_move_valid(board, start, end):
    start_row, start_col = start
    end_row, end_col = end

    piece_char = board[start_row][start_col]
    is_white = piece_char.isupper()

    direction = -1 if is_white else 1
    start_rank = 6 if is_white else 1

    # Standard 1-square forward move
    if start_col == end_col and board[end_row][end_col] == ' ' and start_row + direction == end_row:
        return True

    # Initial 2-square forward move
    if start_col == end_col and start_row == start_rank and board[end_row][end_col] == ' ' and \
       board[start_row + direction][end_col] == ' ' and start_row + 2 * direction == end_row:
        return True

    # Diagonal capture
    if abs(start_col - end_col) == 1 and start_row + direction == end_row and board[end_row][end_col] != ' ':
        # The friendly piece check in is_move_valid already handles capturing your own pieces
        return True

    return False

def is_rook_move_valid(board, start, end):
    start_row, start_col = start
    end_row, end_col = end

    # Must be a purely horizontal or vertical move
    if start_row != end_row and start_col != end_col:
        return False

    # Check for obstructions
    if start_row == end_row: # Horizontal move
        step = 1 if end_col > start_col else -1
        for c in range(start_col + step, end_col, step):
            if board[start_row][c] != ' ':
                return False
    else: # Vertical move
        step = 1 if end_row > start_row else -1
        for r in range(start_row + step, end_row, step):
            if board[r][start_col] != ' ':
                return False

    return True

def is_knight_move_valid(board, start, end):
    start_row, start_col = start
    end_row, end_col = end

    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)

    # Knight moves in an L-shape: {1, 2} or {2, 1}
    return (row_diff == 1 and col_diff == 2) or \
           (row_diff == 2 and col_diff == 1)

def is_bishop_move_valid(board, start, end):
    start_row, start_col = start
    end_row, end_col = end

    # Must be a purely diagonal move
    if abs(start_row - end_row) != abs(start_col - end_col):
        return False

    # Check for obstructions
    row_step = 1 if end_row > start_row else -1
    col_step = 1 if end_col > start_col else -1
    r, c = start_row + row_step, start_col + col_step
    while (r, c) != (end_row, end_col):
        if board[r][c] != ' ':
            return False
        r += row_step
        c += col_step

    return True

def is_queen_move_valid(board, start, end):
    # A queen's move is valid if it's a valid rook move or a valid bishop move.
    return is_rook_move_valid(board, start, end) or \
           is_bishop_move_valid(board, start, end)

def is_king_move_valid(board, start, end):
    start_row, start_col = start
    end_row, end_col = end

    row_diff = abs(start_row - end_row)
    col_diff = abs(start_col - end_col)

    # King can move one square in any direction
    return row_diff <= 1 and col_diff <= 1
