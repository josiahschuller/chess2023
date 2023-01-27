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
        "turn": 0, # 0 for white, 1 for black
    }

    return state

def setup_board(state: Dict):
    """
    Adds pieces to the board in default starting positions
    """
    state_copy = deepcopy(state)

    # Add pawns in one go (so many of them!)
    for col in range(len(state_copy["board"][0])):
        state_copy = add_piece(state=state_copy, piece=pieces.PAWN, row=6, col=col, side=0)
        state_copy = add_piece(state=state_copy, piece=pieces.PAWN, row=1, col=col, side=1)

    # White pieces
    state_copy = add_piece(state=state_copy, piece=pieces.ROOK, row=7, col=0, side=0)
    state_copy = add_piece(state=state_copy, piece=pieces.ROOK, row=7, col=7, side=0)
    state_copy = add_piece(state=state_copy, piece=pieces.BISHOP, row=7, col=2, side=0)
    state_copy = add_piece(state=state_copy, piece=pieces.BISHOP, row=7, col=5, side=0)
    state_copy = add_piece(state=state_copy, piece=pieces.QUEEN, row=7, col=3, side=0)
    state_copy = add_piece(state=state_copy, piece=pieces.KNIGHT, row=7, col=1, side=0)
    state_copy = add_piece(state=state_copy, piece=pieces.KNIGHT, row=7, col=6, side=0)

    # Black pieces
    state_copy = add_piece(state=state_copy, piece=pieces.ROOK, row=0, col=0, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.ROOK, row=0, col=7, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.BISHOP, row=0, col=2, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.BISHOP, row=0, col=5, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.QUEEN, row=0, col=3, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.KNIGHT, row=0, col=1, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.KNIGHT, row=0, col=6, side=1)

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

    id = state_copy["next_id"]
    
    # Create the piece instance (NOTE: should this move to Piece class?)
    if piece == pieces.ROOK:
        piece_obj = pieces.Rook(id=id, row=row, col=col, side=side)
    elif piece == pieces.BISHOP:
        piece_obj = pieces.Bishop(id=id, row=row, col=col, side=side)
    elif piece == pieces.QUEEN:
        piece_obj = pieces.Queen(id=id, row=row, col=col, side=side)
    elif piece == pieces.KNIGHT:
        piece_obj = pieces.Knight(id=id, row=row, col=col, side=side)
    elif piece == pieces.PAWN:
        piece_obj = pieces.Pawn(id=id, row=row, col=col, side=side)
    elif piece == pieces.KING:
        piece_obj = pieces.King(id=id, row=row, col=col, side=side)
    else:
        raise Exception(f"Piece does not exist: {piece}")
    
    # Add piece to the board
    state_copy["board"][row][col] = id
    # Add piece to pieces parameters
    state_copy["pieces_params"][id] = piece_obj
    # Increment next ID
    state_copy["next_id"] += 1

    return state_copy

def replace_piece(state: Dict, id: int, piece: str, row: int, col: int):
    """
    Replaces a piece on the board with another piece (used for promotions).
    Arguments:
    - state: game state
    - pieces_params: pieces parameters
    - id: id of piece to be replaced
    - piece: name of the piece, i.e. "rook", "knight", "bishop", "queen"
    - row: row number
    - col: col number
    Returns: updated game state
    """
    state_copy = deepcopy(state)
    
    if piece == pieces.ROOK:
        piece_obj = pieces.Rook(id=id, row=row, col=col, side=state["pieces_params"][id].side)
    elif piece == pieces.BISHOP:
        piece_obj = pieces.Bishop(id=id, row=row, col=col, side=state["pieces_params"][id].side)
    elif piece == pieces.QUEEN:
        piece_obj = pieces.Queen(id=id, row=row, col=col, side=state["pieces_params"][id].side)
    elif piece == pieces.KNIGHT:
        piece_obj = pieces.Knight(id=id, row=row, col=col, side=state["pieces_params"][id].side)
    
    state_copy["board"][row][col] = id
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
        raise Exception(f"Invalid move: No piece at row={move.start_row}, col={move.start_col}")

    state_copy["pieces_params"][move.piece_id].row = move.end_row
    state_copy["pieces_params"][move.piece_id].col = move.end_col
    
    state_copy["board"][move.end_row][move.end_col] = move.piece_id
    state_copy["board"][move.start_row][move.start_col] = None

    if move.piece_taken is not None:
        # Remove piece from board if piece is still there (used for en passant)
        piece_taken = state_copy["pieces_params"][move.piece_taken]
        if state_copy["board"][piece_taken.row][piece_taken.col] == piece_taken.id:
            state_copy["board"][piece_taken.row][piece_taken.col] = None

        # Add the taken piece to the pieces taken parameters Dict
        state_copy["pieces_taken_params"][move.piece_taken] = piece_taken
        # Remove the piece from the pieces parameters Dict
        state_copy["pieces_params"].pop(move.piece_taken)
    if move.promotion_piece is not None:
        # Replace piece (for promotion)
        state_copy = replace_piece(state=state_copy, id=move.piece_id, piece=move.promotion_piece, row=move.end_row, col=move.end_col)
    
    # Record move in state
    state_copy["moves"].append(move)

    # Record if king has moved
    if isinstance(state_copy["pieces_params"][move.piece_id], pieces.King):
        state_copy["pieces_params"][move.piece_id].has_moved = True
    
    return state_copy

def display_board(state: Dict):
    log_message()
    for row in state["board"]:
        row_str = "|"
        for square in row:
            if square is not None:
                row_str += str(state["pieces_params"][square])
            else:
                row_str += "_"
            row_str += "|"
        log_message(row_str)

def display_pieces(state: Dict):
    for key in state["pieces_params"]:
        log_message(f"{key}: {state['pieces_params'][key].full_str()}")

def get_all_possible_moves(state: Dict) -> List[pieces.Move]:
    """
    Gets all the possible moves
    """
    possible_moves = []
    
    for piece in state["pieces_params"].values():
        if piece.side == state["turn"]:
            possible_moves += piece.get_possible_moves(state=state)
    
    return possible_moves

def choose_move(state: Dict, move_input: str) -> pieces.Move:
    """
    Based on the move input, selects the move from the possible moves
    move_input should be in the form of standard notation (e.g. Ra4)
    """

    # TODO: Check for castling (0-0 and 0-0-0?)
    # TODO: Check for pawn moves (e.g. d4, dxe5, etc.)

    column_letters = "abcdefgh" # Assumes that there are 8 columns
    row_numbers = "87654321" # Assumes that there are 8 rows
    end_col = column_letters.index(move_input[len(move_input)-2])
    end_row = row_numbers.index(move_input[len(move_input)-1])

    # Get the possible moves of that type of piece
    possible_pieces = [piece for piece in state["pieces_params"].values() if piece.side == state["turn"] and str(piece).upper() == move_input[0].upper()]
    possible_moves_with_piece = []
    for piece in possible_pieces:
        possible_moves_with_piece += piece.get_possible_moves(state=state)
    
    # Get the move itself
    possible_moves = []
    for move in possible_moves_with_piece:
        if move.end_row == end_row and move.end_col == end_col:
            possible_moves.append(move)

    # Check for move ambiguity (e.g. if two of the same piece can move to the same square)
    if len(possible_moves) == 1:
        return possible_moves[0]
    elif len(possible_moves) > 1:
        # The move is ambiguous
        if len(move_input) == 4:
            if move_input[1] in column_letters:
                # Disambiguate by column
                for move in possible_moves:
                    if move.start_col == column_letters.index(move_input[1]):
                        return move
                raise Exception("Move is ambiguous and invalid start column letter given")
            elif move_input[1] in row_numbers:
                # Disambiguate by row
                for move in possible_moves:
                    if move.start_row == row_numbers.index(move_input[1]):
                        return move
                raise Exception("Move is ambiguous and invalid start row number given")
            else:
                raise Exception("Move is ambiguous and invalid?")
        else:
            raise Exception("Move is ambiguous")
    else:
        # The move is not valid, so return None
        return None


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
    piece_id = state["board"][start_row][start_col]
    piece_taken = None
    if state["board"][end_row][end_col] is not None:
        piece_taken = state["board"][end_row][end_col]
    
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

def get_user_input(query: str):
    """
    Get the user input. This function is created to make I/O easier to control.
    """
    return input(query)

def log_message(message: str):
    """
    Prints the message. This function is created to make I/O easier to control.
    """
    print(message)

def play(state: Dict):
    """
    Play the game in the terminal
    """
    state_copy = deepcopy(state)

    while len(get_all_possible_moves(state=state_copy)) > 0:
        # Display current state
        display_board(state=state_copy)

        # Get move
        move_input = ""
        move = None
        while move_input == "" or move is None:
            # Ask user for move
            if state_copy["turn"] == 0:
                move_input = get_user_input("White to move: ")
            else:
                move_input = get_user_input("Black to move: ")
        
            if move_input != "":
                # Find move from move input
                try:
                    move = choose_move(state=state_copy, move_input=move_input)
                except:
                    log_message("Invalid move")

        # Make move
        state_copy = make_move(state=state_copy, move=move)

        # Change turn
        state_copy["turn"] = (state_copy["turn"] + 1) % 2
    
    return state_copy

game_state = create_game_state()
game_state = setup_board(state=game_state)
game_state = play(state=game_state)
