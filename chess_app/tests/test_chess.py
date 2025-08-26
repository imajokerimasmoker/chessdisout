import pytest
from chess_app.main import parse_move

def test_parse_move_valid():
    """Tests that valid move strings are parsed correctly."""
    assert parse_move("e2e4") == ((6, 4), (4, 4))
    assert parse_move("a1h8") == ((7, 0), (0, 7))
    assert parse_move("g8f6") == ((0, 6), (2, 5))

def test_parse_move_invalid_length():
    """Tests that move strings of incorrect length raise a ValueError."""
    with pytest.raises(ValueError, match="Move string must be 4 characters long"):
        parse_move("e2e")
    with pytest.raises(ValueError, match="Move string must be 4 characters long"):
        parse_move("e2e4e")

def test_parse_move_invalid_column():
    """Tests that move strings with invalid column characters raise a ValueError."""
    with pytest.raises(ValueError, match="Invalid column character"):
        parse_move("j2e4")
    with pytest.raises(ValueError, match="Invalid column character"):
        parse_move("a1j8")

def test_parse_move_invalid_row_char():
    """Tests that move strings with non-digit row characters raise a ValueError."""
    with pytest.raises(ValueError, match="Invalid row character"):
        parse_move("eaea")

def test_parse_move_row_out_of_bounds():
    """Tests that move strings with out-of-bounds ranks raise a ValueError."""
    with pytest.raises(ValueError, match="Row is out of bounds"):
        parse_move("e9e4")
    with pytest.raises(ValueError, match="Row is out of bounds"):
        parse_move("e0e4")
    with pytest.raises(ValueError, match="Row is out of bounds"):
        parse_move("a1h9")

# --- Move Validation Tests ---
from chess_app.main import is_move_valid, create_board

@pytest.fixture
def board():
    """Provides a standard starting chessboard."""
    return create_board()

def test_rook_valid_moves(board):
    # Test a horizontal move for a white rook
    board[6][0] = ' ' # Clear pawn in front
    board[5][0] = 'R' # Place rook with clear vertical path
    assert is_move_valid(board, (5, 0), (2, 0)) is True

    # Test a horizontal move
    board[3][3] = 'R' # Place rook with clear horizontal path
    assert is_move_valid(board, (3, 3), (3, 7)) is True

def test_rook_invalid_moves(board):
    assert is_move_valid(board, (7, 0), (5, 2)) is False # Diagonal move
    assert is_move_valid(board, (7, 0), (7, 0)) is False # Move to same square (no distance)
    assert is_move_valid(board, (7, 0), (6, 0)) is False # Blocked by own pawn

def test_knight_valid_moves(board):
    assert is_move_valid(board, (7, 1), (5, 0)) is True # White knight initial move
    assert is_move_valid(board, (0, 1), (2, 2)) is True # Black knight initial move

def test_knight_invalid_moves(board):
    assert is_move_valid(board, (7, 1), (6, 3)) is False # Not L-shape
    assert is_move_valid(board, (7, 1), (7, 3)) is False # Not L-shape
    assert is_move_valid(board, (7, 1), (6, 1)) is False # Friendly piece on destination

def test_pawn_valid_moves(board):
    assert is_move_valid(board, (6, 4), (5, 4)) is True # White pawn 1 step
    assert is_move_valid(board, (6, 4), (4, 4)) is True # White pawn 2 steps
    board[5][3] = 'p' # Place black pawn for capture
    assert is_move_valid(board, (6, 4), (5, 3)) is True # White pawn captures

def test_pawn_invalid_moves(board):
    assert is_move_valid(board, (6, 4), (6, 4)) is False # No move
    assert is_move_valid(board, (6, 4), (7, 4)) is False # Move backward
    assert is_move_valid(board, (6, 4), (5, 3)) is False # Diagonal without capture
    board[4][4] = 'P' # Block path for 2-step move
    assert is_move_valid(board, (6, 4), (4, 4)) is False # Blocked 2-step

def test_bishop_valid_moves(board):
    board[6][3] = ' ' # Clear path for white bishop
    assert is_move_valid(board, (7, 2), (4, 5)) is True

def test_bishop_invalid_moves(board):
    assert is_move_valid(board, (7, 2), (6, 2)) is False # Not diagonal
    assert is_move_valid(board, (7, 2), (5, 4)) is False # Blocked by own pawn

def test_queen_valid_moves(board):
    # Set up a scenario for the queen
    board[4][3] = 'Q'

    # Test vertical move
    assert is_move_valid(board, (4, 3), (1, 3)) is True
    # Test horizontal move
    assert is_move_valid(board, (4, 3), (4, 7)) is True
    # Test diagonal move
    assert is_move_valid(board, (4, 3), (1, 6)) is True

def test_king_valid_moves(board):
    board[6][4] = ' ' # Clear path for king
    assert is_move_valid(board, (7, 4), (6, 4)) is True

def test_king_invalid_moves(board):
    assert is_move_valid(board, (7, 4), (5, 4)) is False # Move more than 1 square
    assert is_move_valid(board, (7, 4), (5, 2)) is False # Invalid move
