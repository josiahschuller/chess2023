from typing import Optional, Dict, Tuple, List

class Move:
    def __init__(
        self,
        piece_id: int,
        start_row: int, 
        start_col: int,
        end_row: int,
        end_col: int,
        piece_taken: Optional[int] = None,
        promotion_piece: Optional[str] = None,
        castling_move = None,
    ) -> None:
        """
        Represents a move
        Arguments:
        - piece_id: id of the piece being moved
        - start_row: row number of starting position
        - start_col: column number of starting position
        - end_row: row number of moved position
        - end_col: column number of moved position
        - piece_taken: id of the piece taken, if there is one
        - promotion_piece: name of the piece, i.e. "R", "N", "B", or "Q"
        - castling_move: Move instance of the rook moving
        """
        self.piece_id = piece_id
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece_taken = piece_taken
        self.promotion_piece = promotion_piece
        self.castling_move = castling_move
    
    def __repr__(self):
        return f"Move: ID {self.piece_id} from ({self.start_row}, {self.start_col}) to ({self.end_row}, {self.end_col})"


def move_or_take(state: Dict, potential_squares: Tuple[Tuple[int]], piece) -> List[Move]:
    """
    Generates a list of Moves where the piece either moves or takes until it can't move further.
    This is used for rooks, bishops and queens.
    """
    move_list = []

    for square in potential_squares:
        potential_end_row = square[0]
        potential_end_col = square[1]
        
        if state["board"][potential_end_row][potential_end_col] is None:
            # There is no piece in this square
            move_list.append(Move(
                piece_id=piece.id,
                start_row=piece.row,
                start_col=piece.col,
                end_row=potential_end_row,
                end_col=potential_end_col,
            ))
        else:
            # There is a piece in this square
            if state["pieces_params"][state["board"][potential_end_row][potential_end_col]].side != piece.side:
                # The piece is an opponent piece
                move_list.append(Move(
                    piece_id=piece.id,
                    start_row=piece.row,
                    start_col=piece.col,
                    end_row=potential_end_row,
                    end_col=potential_end_col,
                    piece_taken=state["board"][potential_end_row][potential_end_col]
                ))
            break
    
    return move_list


def get_all_possible_moves(state: Dict, side: int, ignore_complicated: bool = False) -> List[Move]:
    """
    Gets all the possible moves for a particular side
    TODO: Input "ignore_complicated" ignores promotions and castling. This is used for calculating checks.
    """
    possible_moves = []
    
    for piece in state["pieces_params"].values():
        if piece.side == side:
            possible_moves += piece.get_possible_moves(state=state)
    
    return possible_moves
