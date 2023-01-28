import pieces, moves
from typing import Dict, Tuple
from copy import deepcopy

def create_game_state(rows: int = 8, cols: int = 8):
    """
    Creates the game state:
    - board: a layout for the Chess board, containing None for empty squares and the id of a piece for non-empty squares
    - pieces_params: a Dict containing all non-taken pieces where each key is the id of a piece and the value is the instance of the piece
    - pieces_taken_params: same as pieces_params but for taken pieces
    - next_id: id of next piece to be added
    - result: None for game still going, 0 for white wins, 0.5 for draw, 1 for black wins
    - moves: list of moves played
    - positions: list of positions occurred (in FEN)
    - turn: 0 if it's white's turn, 1 if it's black's turn
    """
    state = {
        "board": [[None for _ in range(cols)] for _ in range(rows)],
        "pieces_params": {},
        "pieces_taken_params": {},
        "next_id": 0,
        "result": None,
        "moves": [],
        "positions": [],
        "turn": 0,
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
    state_copy = add_piece(state=state_copy, piece=pieces.KING, row=7, col=4, side=0)

    # Black pieces
    state_copy = add_piece(state=state_copy, piece=pieces.ROOK, row=0, col=0, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.ROOK, row=0, col=7, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.BISHOP, row=0, col=2, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.BISHOP, row=0, col=5, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.QUEEN, row=0, col=3, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.KNIGHT, row=0, col=1, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.KNIGHT, row=0, col=6, side=1)
    state_copy = add_piece(state=state_copy, piece=pieces.KING, row=0, col=4, side=1)

    return state_copy
    
def add_piece(state: Dict, piece: str, row: int, col: int, side: int):
    """
    Adds a piece to the board and to the pieces
    Arguments:
    - state: game state
    - piece: name of the piece, i.e. "P", "R", "N", "B", "Q" or "K"
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

def choose_move(state: Dict, move_input: str) -> moves.Move:
    """
    Based on the move input, selects the move from the possible moves
    move_input should be in the form of standard notation (e.g. Ra4)
    NOTE: pawn moves are represented with a "P" at the start (e.g. Pd4)
    NOTE: taking moves do not have an "x" in them
    """

    # Check for kingside castling
    if move_input == "0-0" or move_input.upper() == "O-O":
        if state["turn"] == 0:
            move_input = "Kg1"
        else:
            move_input = "Kg8"
    # Check for queenside castling
    elif move_input == "0-0-0" or move_input.upper() == "O-O-O":
        if state["turn"] == 0:
            move_input = "Kc1"
        else:
            move_input = "Kc8"
    

    # Check for pawn promotion move (e.g. Pd8=Q)
    promotion_piece = None
    if move_input[-2] == "=":
        promotion_piece = move_input[-1].upper()
        move_input = move_input[:-2]

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
        if move.end_row == end_row and move.end_col == end_col and move.promotion_piece == promotion_piece:
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


def convert_input_to_move(state: Dict, move_input: str) -> moves.Move:
    """
    Converts an input in the form of "{start column letter}{start row number}{end column letter}{end row number}"
    to a Move object.
    NOTE: This is no longer in use.
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

    move = moves.Move(
        piece_id=piece_id,
        start_row=start_row,
        start_col=start_col,
        end_row=end_row,
        end_col=end_col,
        piece_taken=piece_taken,
        promotion_piece=promotion_piece,
    )

    return move

def board_to_fen(state: Dict) -> str:
    """
    Converts board layout to FEN notation (see https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
    """
    fen = ""
    for row in state["board"]:
        spaces = 0
        for square in row:
            if square is not None:
                if spaces > 0:
                    fen += str(spaces)
                    spaces = 0
                fen += str(state["pieces_params"][square])
            else:
                spaces += 1
        if spaces > 0:
            fen += str(spaces)
        fen += "/"
    fen = fen[:-1]
    return fen

def draw_by_insufficient_material(state: Dict) -> bool:
    """
    Checks if a draw by insufficient material has occurred
    """
    # Get strings of pieces on the board
    pieces = [str(piece).upper() for piece in state["pieces_params"].values()]
    
    if len(pieces) == 2:
        # Just 2 kings
        print("Draw by insufficient material")
        return True
    elif len(pieces) == 3:
        if "B" in pieces or "N" in pieces:
            # 2 kings and one bishop/knight
            print("Draw by insufficient material")
            return True
    return False

def draw_by_repetition(state: Dict) -> bool:
    """
    Checks if a draw by repetition has occurred
    """
    position_dict = {}
    for position in state["positions"]:
        if position not in position_dict.keys():
            position_dict[position] = 1
        else:
            position_dict[position] += 1
            if position_dict[position] >= 3:
                print("Draw by repetition")
                return True
                
    return False

def fifty_move_draw(state: Dict) -> bool:
    """
    Checks if a 50 move rule draw has occurred
    """
    total_moves = 50 * 2
    if len(state["moves"]) > total_moves:
        # Iterate through last 50 moves
        for move in state["moves"][len(state["moves"]) - total_moves::]:
            if move.piece_taken is not None:
                # Piece was taken, so no draw
                return False
            for parameters in [state["pieces_params"], state["pieces_taken_params"]]:
                if move.piece_id in parameters:
                    if str(parameters[move.piece_id]).upper() == "P":
                        # Pawn was moved, so no draw
                        return False
        print("Draw by 50 move rule")
        return True
    else:
        return False


def get_user_input(query: str):
    """
    Get the user input. This function is created to make I/O easier to control.
    """
    return input(query)

def log_message(message: str = ""):
    """
    Prints the message. This function is created to make I/O easier to control.
    """
    print(message)

def play(state: Dict) -> Tuple[Dict, float]:
    """
    Play the game in the terminal
    Returns the state as well as the game result: 0 if white wins, 1 if black wins, 0.5 if draw
    """
    state_copy = deepcopy(state)

    while state_copy["result"] is None:
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
        state_copy = pieces.make_move(state=state_copy, move=move)

        # Record position (used for draw by repetition)
        state_copy["positions"].append(board_to_fen(state=state_copy))

        # Change turn
        state_copy["turn"] = (state_copy["turn"] + 1) % 2

        # Check for draws
        if draw_by_insufficient_material(state=state_copy) or draw_by_repetition(state=state_copy) or fifty_move_draw(state=state_copy):
            state_copy["result"] = 0.5
        
        # Check for checkmate or stalemate
        if len(moves.get_all_possible_moves(state=state_copy, side=state["turn"])) == 0:
            if pieces.in_check(state=state_copy, side=state["turn"]):
                # Checkmate
                if state["turn"] == 0:
                    state_copy["result"] = 1
                else:
                    state_copy["result"] = 0
            else:
                # Stalemate
                print("Draw by stalemate")
                state_copy["result"] = 0.5

    return state_copy

if __name__ == "__main__":
    # Set up game
    game_state = create_game_state()
    game_state = setup_board(state=game_state)

    # Play game
    game_state = play(state=game_state)

    # Display result
    display_board(state=game_state)
    log_message(game_state["result"])
