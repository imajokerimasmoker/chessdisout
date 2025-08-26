from flask import Flask, render_template, request, redirect, url_for, session
from chess_app import main as chess_logic

app = Flask(__name__)
app.secret_key = 'a very secret key for session management'

# --- Game State Management ---
def start_new_game():
    """Initializes a new game in the session."""
    session['board'] = chess_logic.create_board()
    session['turn'] = 'white'
    session['error'] = None

# --- Unicode Pieces ---
PIECE_UNICODE = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    ' ': ' '
}

# --- HTML Generation ---
def board_to_html_table(board):
    """Converts the board representation to an HTML table."""
    html = "<table>"
    for r_idx, row in enumerate(board):
        html += "<tr>"
        for c_idx, piece in enumerate(row):
            color = "white" if (r_idx + c_idx) % 2 == 0 else "black"
            html += f"<td class='{color}'>{PIECE_UNICODE.get(piece, ' ')}</td>"
        html += "</tr>"
    html += "</table>"
    return html

# --- Routes ---
@app.route('/')
def index():
    """Renders the main page with the chessboard."""
    if 'board' not in session:
        start_new_game()

    board_html = board_to_html_table(session['board'])
    # Get the error from the session and then clear it.
    current_error = session.pop('error', None)
    return render_template('index.html', board_table=board_html, turn=session['turn'], error=current_error)

@app.route('/move', methods=['POST'])
def move():
    """Handles a move submitted by the player."""
    from_square = request.form.get('from_square', '').strip().lower()
    to_square = request.form.get('to_square', '').strip().lower()

    if not from_square or not to_square:
        session['error'] = "Both 'From' and 'To' fields are required."
        return redirect(url_for('index'))

    move_str = from_square + to_square

    try:
        start_pos, end_pos = chess_logic.parse_move(move_str)
        # We need to get the board from the session, make a move, and save it back
        current_board = session['board']
        updated_board = chess_logic.make_move(current_board, start_pos, end_pos, session['turn'])
        session['board'] = updated_board

        # Switch turns
        session['turn'] = 'black' if session['turn'] == 'white' else 'white'
        session['error'] = None
    except ValueError as e:
        session['error'] = str(e)

    return redirect(url_for('index'))

@app.route('/new', methods=['POST'])
def new_game():
    """Starts a new game."""
    start_new_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
