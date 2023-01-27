from typing import List, Dict
import moves

ROOK = "R"
BISHOP = "B"
QUEEN = "Q"
KNIGHT = "N"
PAWN = "P"
KING = "K"


class Piece:
    def __init__(self, id: int, row: int, col: int, side: int) -> None:
        self.id = id
        self.row = row
        self.col = col
        self.side = side # 0 for white, 1 for black

    def get_possible_moves(self) -> List[moves.Move]:
        pass
    
    def full_str(self):
        return f"{self.__repr__()} at ({self.row}, {self.col})"

class Rook(Piece):
    def get_possible_moves(self, state: Dict) -> List[moves.Move]:
        move_list = []

        # Add vertical moves up
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row-1, -1, -1))
        move_list += moves.move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add vertical moves down
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row + 1, len(state["board"])))
        move_list += moves.move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the left
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col-1, -1, -1))
        move_list += moves.move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the right
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col + 1, len(state["board"][0])))
        move_list += moves.move_or_take(
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
    def get_possible_moves(self, state: Dict) -> List[moves.Move]:
        move_list = []

        # Add diagonal moves down left
        potential_rows = [row for row in range(self.row - 1, -1, -1)]
        potential_cols = [col for col in range(self.col - 1, -1, -1)]
        # Shorten the lists to the same length
        potential_rows = potential_rows[0:min(len(potential_rows), len(potential_cols))]
        potential_cols = potential_cols[0:min(len(potential_rows), len(potential_cols))]
        # Zip them
        potential_squares = tuple(zip(potential_rows, potential_cols))
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
    def get_possible_moves(self, state: Dict) -> List[moves.Move]:
        
        move_list = []

        # Add vertical moves up
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row-1, -1, -1))
        move_list += moves.move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add vertical moves down
        potential_squares = ((potential_row, self.col) for potential_row in range(self.row + 1, len(state["board"])))
        move_list += moves.move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the left
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col-1, -1, -1))
        move_list += moves.move_or_take(
            state=state,
            potential_squares=potential_squares,
            piece=self,
        )

        # Add horizontal moves to the right
        potential_squares = ((self.row, potential_col) for potential_col in range(self.col + 1, len(state["board"][0])))
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
        move_list += moves.move_or_take(
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
    def get_possible_moves(self, state: Dict) -> List[moves.Move]:
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
                move_list.append(moves.Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=potential_end_row,
                    end_col=potential_end_col,
                ))
            elif state["pieces_params"][state["board"][potential_end_row][potential_end_col]].side != self.side:
                move_list.append(moves.Move(
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
    def get_possible_moves(self, state: Dict) -> List[moves.Move]:
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
                    move_list.append(moves.Move(
                        piece_id=self.id,
                        start_row=self.row,
                        start_col=self.col,
                        end_row=self.row + direction,
                        end_col=self.col,
                        promotion_piece=piece
                    ))
            else:
                move_list.append(moves.Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=self.row + direction,
                    end_col=self.col,
                ))

            # Add moves for going forward 2 squares
            if self.row == start_row and state["board"][self.row + 2*direction][self.col] is None:
                move_list.append(moves.Move(
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
                            move_list.append(moves.Move(
                                piece_id=self.id,
                                start_row=self.row,
                                start_col=self.col,
                                end_row=self.row + direction,
                                end_col=end_col,
                                piece_taken=square_to_take,
                                promotion_piece=piece,
                            ))
                    else:
                        move_list.append(moves.Move(
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
                                move_list.append(moves.Move(
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

    def get_possible_moves(self, state: Dict) -> List[moves.Move]:
        move_list = []

        # Squares around itself
        possible_squares = []
        # Row above
        if self.row >= 1:
            possible_squares.append((self.row - 1, self.col))
            if self.col >= 1:
                possible_squares.append((self.row - 1, self.col - 1))
            if self.col <= 6:
                possible_squares.append((self.row - 1, self.col + 1))
        # Row below
        if self.row <= 6:
            possible_squares.append((self.row + 1, self.col))
            if self.col >= 1:
                possible_squares.append((self.row + 1, self.col - 1))
            if self.col <= 6:
                possible_squares.append((self.row + 1, self.col + 1))
        # Same row
        if self.col >= 1:
            possible_squares.append((self.row, self.col - 1))
        if self.col <= 6:
            possible_squares.append((self.row, self.col + 1))
        
        for square in possible_squares:
            potential_end_row = square[0]
            potential_end_col = square[1]

            if state["board"][potential_end_row][potential_end_col] is None:
                move_list.append(moves.Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=potential_end_row,
                    end_col=potential_end_col,
                ))
            elif state["pieces_params"][state["board"][potential_end_row][potential_end_col]].side != self.side:
                move_list.append(moves.Move(
                    piece_id=self.id,
                    start_row=self.row,
                    start_col=self.col,
                    end_row=potential_end_row,
                    end_col=potential_end_col,
                    piece_taken=state["board"][potential_end_row][potential_end_col]
                ))

        # Castling
        if not self.has_moved:
            for rook_col in [0, len(state["board"][0]) - 1]:
                pieces_between = False
                # Check if there are any pieces between the king and rook
                for col in range(min(self.col, rook_col) + 1, max(self.col, rook_col)):
                    if state["board"][self.row][col] is not None:
                        pieces_between = True
                
                if not pieces_between:
                    if rook_col == 0:
                        king_final_col = self.col - 2
                        rook_final_col = self.col - 1
                    else:
                        king_final_col = self.col + 2
                        rook_final_col = self.col + 1
                    
                    # Check that there are no opponent pieces that threaten the path of castling
                    castling_path_safe = True                        
                    for col in range(min(self.col, king_final_col) + 1, max(self.col, king_final_col)):
                        # TODO: Check for checks in these squares!
                        pass
                    
                    if castling_path_safe:
                        # Add move to castle
                        move_list.append(moves.Move(
                            piece_id=self.id,
                            start_row=self.row,
                            start_col=self.col,
                            end_row=self.row,
                            end_col=king_final_col,
                            castling_move=moves.Move(
                                piece_id=state["board"][self.row][rook_col],
                                start_row=self.row,
                                start_col=rook_col,
                                end_row=self.row,
                                end_col=rook_final_col
                            )
                        ))

        return move_list
    
    def __repr__(self):
        if self.side == 0:
            return "K"
        else:
            return "k"

