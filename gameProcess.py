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
        self.__turn = "b"
        self.__chess_board = ChessBoard(x=10,
                                        y=10,
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
        b_king = King(2, 2, "b")
        b_king1 = King(2, 3, "b")
        b_king2 = King(6, 7, "b")
        self.__chess_board.add_piece(b_king)
        self.__chess_board.add_piece(b_king1)
        self.__chess_board.add_piece(b_king2)
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
                                # print(self.__field[y][x], x, y, "DEACTIVADED")
                    else:
                        # print(f"out_of_board! {x, y}")
                        pass

            pygame.display.update()
