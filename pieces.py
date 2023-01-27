from typing import List, Dict, Tuple, Optional

ROOK = "rook"
BISHOP = "bishop"
QUEEN = "queen"
KNIGHT = "knight"
PAWN = "pawn"
KING = "king"

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
        - promotion_piece: name of the piece, i.e. "rook", "knight", "bishop", or "queen"
        """
        self.piece_id = piece_id
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.piece_taken = piece_taken
        self.promotion_piece = promotion_piece
    
    def __repr__(self):
        return f"Move: ID {self.piece_id} from ({self.start_row}, {self.start_col}) to ({self.end_row}, {self.end_col})"


class Piece:
    def __init__(self, id: int, row: int, col: int, side: int) -> None:
        self.id = id
        self.row = row
        self.col = col
        self.side = side # 0 for white, 1 for black

    def get_possible_moves(self) -> List[Move]:
        pass
    
    def full_str(self):
        return f"{self.__repr__()} at ({self.row}, {self.col})"

class Rook(Piece):
    def get_possible_moves(self, state: Dict) -> List[Move]:
        move_list = []

        # Add vertical moves up
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row-1, -1, -1))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add vertical moves down
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row + 1, len(state["board"])))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the left
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col-1, -1, -1))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the right
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col + 1, len(state["board"][0])))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        return move_list
    
    def __repr__(self):
        if self.side == 0:
            return "R"
        else:
            return "r"

class Bishop(Piece):
    def get_possible_moves(self, state: Dict) -> List[Move]:
        move_list = []

        # Add diagonal moves down left
        potential_rows = [row for row in range(self.row - 1, -1, -1)]
        potential_cols = [col for col in range(self.col - 1, -1, -1)]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves down right
        potential_rows = [row for row in range(self.row - 1, -1, -1)]
        potential_cols = [col for col in range(self.col + 1, len(state["board"][0]))]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves up left
        potential_rows = [row for row in range(self.row + 1, len(state["board"]))]
        potential_cols = [col for col in range(self.col - 1, -1, -1)]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves up right
        potential_rows = [row for row in range(self.row + 1, len(state["board"]))]
        potential_cols = [col for col in range(self.col + 1, len(state["board"][0]))]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        return move_list
    
    def __repr__(self):
        if self.side == 0:
            return "B"
        else:
            return "b"

class Queen(Piece):
    def get_possible_moves(self, state: Dict) -> List[Move]:
        
        move_list = []

        # Add vertical moves up
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row-1, -1, -1))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add vertical moves down
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row + 1, len(state["board"])))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the left
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col-1, -1, -1))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the right
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col + 1, len(state["board"][0])))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves down left
        potential_rows = [row for row in range(self.row - 1, -1, -1)]
        potential_cols = [col for col in range(self.col - 1, -1, -1)]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves down right
        potential_rows = [row for row in range(self.row - 1, -1, -1)]
        potential_cols = [col for col in range(self.col + 1, len(state["board"][0]))]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves up left
        potential_rows = [row for row in range(self.row + 1, len(state["board"]))]
        potential_cols = [col for col in range(self.col - 1, -1, -1)]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add diagonal moves up right
        potential_rows = [row for row in range(self.row + 1, len(state["board"]))]
        potential_cols = [col for col in range(self.col + 1, len(state["board"][0]))]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        return move_list
    
    def __repr__(self):
        if self.side == 0:
            return "Q"
        else:
            return "q"

class Knight(Piece):
    def get_possible_moves(self, state: Dict) -> List[Move]:
        move_list = []

        # Add all squares the knight can reach
        potential_squares = []
        if self.row >= 1:
            if self.col >= 2:
                potential_squares.append((self.row - 1, self.col - 2))
            if self.col <= len(state["board"][0]) - 3:
                potential_squares.append((self.row - 1, self.col + 2))
        
        if self.row >= 2:
            if self.col >= 1:
                potential_squares.append((self.row - 2, self.col - 1))
            if self.col <= len(state["board"][0]) - 2:
                potential_squares.append((self.row - 2, self.col + 1))
        
        if self.row <= len(state["board"]) - 2:
            if self.col >= 2:
                potential_squares.append((self.row + 1, self.col - 2))
            if self.col <= len(state["board"][0]) - 3:
                potential_squares.append((self.row + 1, self.col + 2))
        
        if self.row <= len(state["board"]) - 3:
            if self.col >= 1:
                potential_squares.append((self.row + 2, self.col - 1))
            if self.col <= len(state["board"][0]) - 2:
                potential_squares.append((self.row + 2, self.col + 1))

        # Add the possible moves 
        for square in potential_squares:
            potential_end_row = square[0]
            potential_end_col = square[1]

            if state["board"][potential_end_row][potential_end_col] is None:
                move_list.append(Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=potential_end_row,
                    end_col=potential_end_col,
                ))
            elif state["pieces_params"][state["board"][potential_end_row][potential_end_col]].side != self.side:
                move_list.append(Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=potential_end_row,
                    end_col=potential_end_col,
                    piece_taken=state["board"][potential_end_row][potential_end_col]
                ))

        return move_list
    
    def __repr__(self):
        if self.side == 0:
            return "N"
        else:
            return "n"

class Pawn(Piece):
    def get_possible_moves(self, state: Dict) -> List[Move]:
        move_list = []

        potential_move_squares = []
        potential_take_squares = []

        # Set direction of where pawns go (up for White, down for Black)
        # Set start row for pawns
        # Set final row for pawns (where they promote)
        if self.side == 0:
            direction = -1
            start_row = len(state["board"]) - 2
            final_row = 0
        else:
            direction = 1
            start_row = 1
            final_row = len(state["board"])
        
        # Pieces to promote to
        promotion_pieces = [KNIGHT, BISHOP, ROOK, QUEEN]
            
        # Add moves for going forward
        if state["board"][self.row + direction][self.col] is None:
            # Add moves for going forward 1 square
            
            # Check if the move will promote the pawn
            if self.row == final_row - direction:
                # Add moves for promotions
                for piece in promotion_pieces:
                    move_list.append(Move(
                        piece_id=self.id,
                        start_row=self.row,
                        start_col=self.col,
                        end_row=self.row + direction,
                        end_col=self.col,
                        promotion_piece=piece
                    ))
            else:
                move_list.append(Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=self.row + direction,
                    end_col=self.col,
                ))

            # Add moves for going forward 2 squares
            if self.row == start_row and state["board"][self.row + 2*direction][self.col] is None:
                move_list.append(Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=self.row + 2*direction,
                    end_col=self.col,
                ))

        # Add moves for taking diagonally
        for end_col in [self.col - 1, self.col + 1]:
            if end_col >= 0 and end_col < len(state["board"][0]):
                square_to_take = state["board"][self.row + direction][end_col]
                if square_to_take is not None and state["pieces_params"][square_to_take].side != self.side:
                    # Check if the move will become a promotion
                    if self.row == final_row - direction:
                        # Add moves for promotions
                        for piece in promotion_pieces:
                            move_list.append(Move(
                                piece_id=self.id,
                                start_row=self.row,
                                start_col=self.col,
                                end_row=self.row + direction,
                                end_col=end_col,
                                piece_taken=square_to_take,
                                promotion_piece=piece,
                            ))
                    else:
                        move_list.append(Move(
                            piece_id=self.id,
                            start_row=self.row,
                            start_col=self.col,
                            end_row=self.row + direction,
                            end_col=end_col,
                            piece_taken=square_to_take,
                        ))

                # Add moves for en passant
                if len(state["moves"]) > 0:
                    # Get the last move played
                    last_move = state["moves"][-1]
                    if last_move.end_row == self.row and last_move.end_col == end_col:
                        # Last move ended on the square next to this pawn
                        if str(state["pieces_params"][last_move.piece_id]).upper() == "P":
                            # Last move was a pawn moving to a square next to this pawn
                            if abs(last_move.start_row - last_move.end_row) == 2:
                                # Last move was a pawn moving forward 2 squares to a square next to this pawn
                                move_list.append(Move(
                                    piece_id=self.id,
                                    start_row=self.row,
                                    start_col=self.col,
                                    end_row=self.row + direction,
                                    end_col=end_col,
                                    piece_taken=last_move.piece_id,
                                ))


        return move_list
    
    def __repr__(self):
        if self.side == 0:
            return "P"
        else:
            return "p"

class King(Piece):
    def __init__(self, id: int, row: int, col: int, side: int) -> None:
        super().__init__(id=id, row=row, col=col, side=side)
        self.has_moved = False

    def get_possible_moves(self) -> List[Move]:
        pass
    
    def __repr__(self):
        if self.side == 0:
            return "K"
        else:
            return "k"


def move_or_take(state: Dict, potential_squares: Tuple[Tuple[int]], piece: Piece) -> List[Move]:
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
