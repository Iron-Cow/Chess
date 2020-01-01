from models import *
import pygame


class GameProcess(object):
    def __init__(self):
        self.__run = True
        self.__field = [[0 for __ in range(8)] for _ in range(8)]
        self.__cell_size = 60
        self.__window = pygame.display.set_mode(size=(900, 600))
        self.__active_tile = None
        self._possible_moves = []
        self.__turn = "w"
        self.__chess_board = ChessBoard(x=50,
                                        y=50,
                                        cell_size=self.__cell_size,
                                        surface=self.__window,
                                        field=self.__field)

    def set_active_tile(self, active_tile_value: tuple or None):
        self.__active_tile = active_tile_value
        self.__chess_board.set_active_tile(active_tile_value)

    def set_possible_moves(self, possible_moves: list):
        self._possible_moves = possible_moves
        self.__chess_board.set_possible_moves(possible_moves)

    def is_check(self, field: list):
        """True if given field checks the current player's King"""

        def find_my_king(field: list) -> tuple:
            """:returns tuple of coordinates of the King on corresponding turn"""
            for i, row in enumerate(field):
                for j, el in enumerate(row):
                    if el != 0 and el.color == self.__turn and el.symbol == "K":
                        return field[i][j].tiles

        def all_enemy_hits(field_option: list) -> list:
            """:returns the list of all tiles that enemy can hit or reach on given board"""
            enemy_hits = []
            for i, row in enumerate(field_option):
                for j, el in enumerate(row):
                    if el != 0 and el.color != self.__turn:
                        enemy_hits += el.get_possible_moves(field_option)
            return sorted(list(set(enemy_hits)))  # sort for debug only

        return find_my_king(field) in all_enemy_hits(field)

    def event_checker(self):
        for event in pygame.event.get():  # key mapping of the game
            # print(event)
            if event.type == pygame.QUIT:
                self.__run = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = self.__chess_board.get_tiles(event)  # index of clicked cell

                if len(self.__turn) > 1:  # Pawn transformation active
                    if x == 8:
                        pieces = [Queen, Knight, Bishop, Rook]
                        for i in range(4):
                            if y == 2+i:
                                self.__chess_board.add_piece(pieces[i](self.__active_tile[0],
                                                                  self.__active_tile[1],
                                                                  self.__turn[0]))
                                if self.__turn[0] == "b":
                                    self.__turn = "w"
                                else:
                                    self.__turn = "b"
                                self.set_active_tile(None)
                                self.__field = self.__chess_board.get_field()

                                break

                elif 0 <= x <= 7 and 0 <= y <= 7:
                    # print(x, y)
                    if not self.__active_tile:
                        if self.__field[y][x] != 0 and self.__field[y][x].color == self.__turn:
                            possible_moves = self.__field[y][x].get_possible_moves(self.__field)
                            self.set_active_tile((x, y))

                            # Check if my move will not cause the check
                            possible_moves_without_check = []
                            for move in possible_moves:
                                field_to_check = self.__chess_board.make_field_prediction(move)
                                if not self.is_check(field_to_check):
                                    possible_moves_without_check.append(move)
                            self.set_possible_moves(possible_moves_without_check)

                        else:
                            pass

                    else:  # if active tile is activated
                        if (x, y) == self.__active_tile:  # remove activation
                            self.set_active_tile(None)
                            self.set_possible_moves([])
                        elif (x, y) in self._possible_moves:  # make a move

                            # PAWN TRANSFORMATION BLOCK
                            if (y == 0 or y == len(self.__field)) and \
                                    self.__field[self.__active_tile[1]][self.__active_tile[0]].symbol == "P":
                                print("TRANSFORMATION!!!!", x, y)
                                self.__turn = f"{self.__turn}T"
                                print(self.__turn)
                                self.__chess_board.make_move((x, y))
                                self.__field = self.__chess_board.get_field()
                                self.set_active_tile((x, y))

                            if len(self.__turn) == 1:
                                self.__chess_board.make_move((x, y))
                                if self.__turn == "b":
                                    self.__turn = "w"
                                else:
                                    self.__turn = "b"
                                self.set_active_tile(None)
                                self.__field = self.__chess_board.get_field()

                            self.set_possible_moves([])
                            # print(self.__field[y][x], x, y, "DEACTIVADED")
                else:
                    # print(f"out_of_board! {x, y}")
                    pass

    def chess_board_fill(self):
        self.__chess_board.add_piece(Rook(7, 0, "b"))
        self.__chess_board.add_piece(Knight(6, 0, "b"))
        self.__chess_board.add_piece(Bishop(5, 0, "b"))
        self.__chess_board.add_piece(King(4, 0, "b"))
        self.__chess_board.add_piece(Queen(3, 0, "b"))
        self.__chess_board.add_piece(Bishop(2, 0, "b"))
        self.__chess_board.add_piece(Knight(1, 0, "b"))
        self.__chess_board.add_piece(Rook(0, 0, "b"))
        [self.__chess_board.add_piece(Pawn(i, 1, "b")) for i in range(8)]

        self.__chess_board.add_piece(Rook(7, 7, "w"))
        self.__chess_board.add_piece(Knight(6, 7, "w"))
        self.__chess_board.add_piece(Bishop(5, 7, "w"))
        self.__chess_board.add_piece(King(4, 7, "w"))
        self.__chess_board.add_piece(Queen(3, 7, "w"))
        self.__chess_board.add_piece(Bishop(2, 7, "w"))
        self.__chess_board.add_piece(Knight(1, 7, "w"))
        self.__chess_board.add_piece(Rook(0, 7, "w"))
        [self.__chess_board.add_piece(Pawn(i, 6, "w")) for i in range(8)]

    def start(self):

        pygame.init()
        self.chess_board_fill()
        while self.__run:
            self.__window.fill((50, 90, 50))
            self.__chess_board.draw_board()
            if len(self.__turn) > 1:
                self.__chess_board.draw_transformation_options(self.__turn[0], self.__window)
            self.__chess_board.draw_all_pieces()
            self.__field = self.__chess_board.get_field()
            self.event_checker()

            pygame.display.update()
