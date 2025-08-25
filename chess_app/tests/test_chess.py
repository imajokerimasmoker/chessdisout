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
