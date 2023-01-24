from typing import List, Dict, Optional

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
        - promotion_piece: name of the piece, i.e. "pawn", "rook", "knight", "bishop", "queen" or "king"
        """
        self.piece_id = piece_id
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece_taken = piece_taken
        self.promotion_piece = promotion_piece


class Piece:
    def __init__(self, id: int, row: int, col: int, side: int) -> None:
        self.id = id
        self.row = row
        self.col = col
        self.side = side # 0 for white, 1 for black

    def possible_moves(self) -> List[Move]:
        pass
    
    def full_str(self):
        return f"{self.__repr__()} at ({self.row}, {self.col})"

class Rook(Piece):
    def __init__(self, id: int, row: int, col: int, side: int) -> None:
        super().__init__(id=id, row=row, col=col, side=side)

    def possible_moves(self) -> List[Move]:
        pass
    
    def __repr__(self):
        if self.side == 0:
            return "R"
        else:
            return "r"

class Queen(Piece):
    def __init__(self, id: int, row: int, col: int, side: int) -> None:
        super().__init__(id=id, row=row, col=col, side=side)

    def possible_moves(self) -> List[Move]:
        pass
    
    def __repr__(self):
        if self.side == 0:
            return "Q"
        else:
            return "q"