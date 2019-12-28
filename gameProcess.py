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

    def start(self):
        self.__window.fill((50, 90, 50))
        pygame.init()
        # b_king = King(2, 2, "b")
        # w_king = King(5, 7, "w")
        # b_pawn1 = Pawn(4, 4, "b")
        # b_pawn2 = Pawn(5, 4, "b")
        # b_pawn3 = Pawn(5, 5, "b")
        # w_pawn1 = Pawn(6, 6, "w")
        # w_rook1 = Rook(4, 2, "w")
        # w_bishop1 = Bishop(5, 2, "w")
        # w_queen1 = Queen(1, 1, "w")
        # w_knight1 = Knight(2, 5, "w")
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



        # self.__chess_board.add_piece(w_king)
        # self.__chess_board.add_piece(b_pawn1)
        # self.__chess_board.add_piece(b_pawn2)
        # self.__chess_board.add_piece(b_pawn3)
        # self.__chess_board.add_piece(w_pawn1)
        # self.__chess_board.add_piece(w_rook1)
        # self.__chess_board.add_piece(w_bishop1)
        # self.__chess_board.add_piece(w_queen1)
        # self.__chess_board.add_piece(w_knight1)
        while self.__run:
            self.__chess_board.draw_board()
            self.__chess_board.draw_all_pieces()
            self.__field = self.__chess_board.get_field()

# ######### CREATE EVENT CHECKER ##############

            for event in pygame.event.get():  # key mapping of the game
                # print(event)
                # print(event)
                if event.type == pygame.QUIT:
                    self.__run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = self.__chess_board.get_tiles(event)  # index of clicked cell
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        # print(x, y)
                        if not self.__active_tile:
                            if self.__field[y][x] != 0 and self.__field[y][x].color == self.__turn:
                                possible_moves = self.__field[y][x].get_possible_moves(self.__field)
                                # print(self.__field[y][x], x, y, "ACTIVADED")
                                self.set_active_tile((x, y))
                                self.set_possible_moves(possible_moves)

                            else:
                                pass
                        else:  # if active tile is activated
                            if (x, y) == self.__active_tile:
                                self.set_active_tile(None)
                                self.set_possible_moves([])
                            elif (x, y) in self._possible_moves:
                                self.__chess_board.make_move((x, y))

                                if self.__turn == "b":
                                    self.__turn = "w"
                                else:
                                    self.__turn = "b"
                                self.set_active_tile(None)
                                self.set_possible_moves([])
                                self.__field = self.__chess_board.get_field()
                                # print(self.__field[y][x], x, y, "DEACTIVADED")
                    else:
                        # print(f"out_of_board! {x, y}")
                        pass

            pygame.display.update()
