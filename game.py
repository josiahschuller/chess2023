import pieces
from typing import List, Dict
from copy import deepcopy

def create_game_state(rows: int = 8, cols: int = 8):
    state = {
        "board": [[None for _ in range(cols)] for _ in range(rows)],
        "pieces_params": {},
        "pieces_taken_params": {},
        "next_id": 0,
        "result": None, # 0 for white wins, 0.5 for draw, 1 for black wins
        "moves": [],
        "king_has_moved": [False, False], # [white, black]
        "turn": 0, # 0 for white, 1 for black
    }

    return state

def setup_board(state: Dict):
    """
    Adds pieces to the board in default starting positions
    """
    state_copy = deepcopy(state)

    state_copy = add_piece(state=state_copy, piece="rook", row=7, col=0, side=0)
    state_copy = add_piece(state=state_copy, piece="queen", row=7, col=3, side=0)

    return state_copy
    
def add_piece(state: Dict, piece: str, row: int, col: int, side: int):
    """
    Adds a piece to the board and to the pieces
    Arguments:
    - state: game state
    - piece: name of the piece, i.e. "pawn", "rook", "knight", "bishop", "queen" or "king"
    - row: row number
    - col: col number
    - side: 0 for white, 1 for black
    Returns: updated game state
    """
    state_copy = deepcopy(state)
    
    if piece == "rook":
        piece_obj = pieces.Rook(id=state_copy["next_id"], row=row, col=col, side=side)
    elif piece == "queen":
        piece_obj = pieces.Queen(id=state_copy["next_id"], row=row, col=col, side=side)
    
    state_copy["board"][row][col] = piece_obj
    state_copy["pieces_params"][state_copy["next_id"]] = piece_obj
    
    state_copy["next_id"] += 1

    return state_copy

def replace_piece(state: Dict, id: int, piece: str, row: int, col: int):
    """
    Replaces a piece on the board with another piece (used for promotions).
    Arguments:
    - state: game state
    - pieces_params: pieces parameters
    - id: id of piece to be replaced
    - piece: name of the piece, i.e. "pawn", "rook", "knight", "bishop", "queen" or "king"
    - row: row number
    - col: col number
    Returns: updated game state
    """
    state_copy = deepcopy(state)
    
    if piece == "rook":
        piece_obj = pieces.Rook(id=id, row=row, col=col, side=state["pieces_params"][id].side)
    elif piece == "queen":
        piece_obj = pieces.Queen(id=id, row=row, col=col, side=state["pieces_params"][id].side)
    
    state_copy["board"][row][col] = piece_obj
    state_copy["pieces_params"][id] = piece_obj
    
    return state_copy

def make_move(state: Dict, move: pieces.Move):
    """
    Makes a move. Returns new board and pieces
    Arguments:
    - state: game state
    - move: Move object
    Returns: updated game state
    """
    state_copy = deepcopy(state)
    
    if state_copy["board"][move.start_row][move.start_col] is None:
        print(state_copy["board"])
        raise Exception(f"Invalid move: No piece at row={move.start_row}, col={move.start_col}")

    state_copy["pieces_params"][move.piece_id].row = move.end_row
    state_copy["pieces_params"][move.piece_id].col = move.end_col
    
    state_copy["board"][move.end_row][move.end_col] = state_copy["pieces_params"][move.piece_id]
    state_copy["board"][move.start_row][move.start_col] = None

    if move.piece_taken is not None:
        # Add the taken piece to the pieces taken parameters Dict
        state_copy["pieces_taken_params"][move.piece_taken] = state_copy["pieces_params"][move.piece_taken]
        # Remove the piece from the pieces parameters Dict
        state_copy["pieces_params"].pop(move.piece_taken)
    if move.promotion_piece is not None:
        # Replace piece (for promotion)
        state_copy = replace_piece(state=state_copy, id=move.piece_id, piece=move.promotion_piece, row=move.end_row, col=move.end_col)
    
    # Record move in state
    state_copy["moves"].append(move)

    # Record if king has moved
    if isinstance(state_copy["pieces_params"][move.piece_id], pieces.King):
        state_copy["king_has_moved"][state_copy["pieces_params"][move.piece_id].side] = True
    
    return state_copy

def display_board(state: Dict):
    for row in state["board"]:
        print(row)

def display_pieces(state: Dict):
    for key in state["pieces_params"]:
        print(f"{key}: {state['pieces_params'][key].full_str()}")

def convert_input_to_move(state: Dict, move_input: str) -> pieces.Move:
    """
    Converts an input in the form of "{start column letter}{start row number}{end column letter}{end row number}"
    to a Move object.
    I am not sure how long I will use this for,
    because in future, each move will be chosen
    from a list of available moves.
    """
    column_letters = "abcdefgh"
    row_numbers = "87654321"

    start_col = column_letters.index(move_input[0])
    start_row = row_numbers.index(move_input[1])
    end_col = column_letters.index(move_input[2])
    end_row = row_numbers.index(move_input[3])
    piece_id = state["board"][start_row][start_col].id
    piece_taken = None
    if state["board"][end_row][end_col] is not None:
        piece_taken = state["board"][end_row][end_col].id
    
    promotion_piece = None # ?

    move = pieces.Move(
        piece_id=piece_id,
        start_row=start_row,
        start_col=start_col,
        end_row=end_row,
        end_col=end_col,
        piece_taken=piece_taken,
        promotion_piece=promotion_piece,
    )

    return move

def play(state: Dict):
    state_copy = deepcopy(state)

    while state_copy["result"] is None:
        # Display current state
        print()
        display_board(state=state_copy)
        display_pieces(state=game_state)

        # Ask for move
        if state_copy["turn"] == 0:
            move_input = input("White to move: ")
        else:
            move_input = input("Black to move: ")
        move = convert_input_to_move(state=state_copy, move_input=move_input)

        # Make move
        state_copy = make_move(state=state_copy, move=move)
    
    return state_copy

game_state = create_game_state()
game_state = setup_board(state=game_state)
game_state = play(state=game_state)


"""
TODO: Removing piece from piece_params is not working?
TODO: Make display_board look nicer
TODO: Ask for user input again if no input is provided (or if the input is invalid)
TODO: Make sure that the right colour piece is moved (i.e. a black piece isn't moved on White's turn)
"""