import pygame
from abc import ABC, abstractmethod
from PIL import Image


class RectField(object):
    """
    Rectangle in pygame.
    """

    def __init__(self, x: float, y: float, width: float, height: float, surface, color: tuple = (0, 0, 0)):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._surface = surface
        self._color = color

    def draw(self):
        pygame.draw.rect(self._surface, self._color, [self._x, self._y, self._width, self._height])

    def get_w(self):
        return self._width


class Piece(ABC):
    def __init__(self, x_tile: int, y_tile: int, color: str, symbol: str):
        self._symbol = symbol
        self._moves_count = 0
        self._x_tile = x_tile
        self._y_tile = y_tile
        self._color = color
        self._figure_pic = pygame.image.load(f"img/{self.color}{self._symbol}.png")
        self._DIRECTIONS = {
            "N": (0, -1),
            "NE": (1, -1),
            "E": (1, 0),
            "SE": (1, 1),
            "S": (0, 1),
            "SW": (-1, 1),
            "W": (-1, 0),
            "NW": (-1, -1)
        }
        self.directions_change()

    def directions_change(self):

        if self.color == "b":
            new_directions = self._DIRECTIONS
            for k in self._DIRECTIONS:
                if k[0] == "N" or k[0] == "S":
                    val = self._DIRECTIONS[k]
                    new_val = (val[0], -1 * val[1])
                    new_directions[k] = new_val

    def set_new_tile(self, new_tile: tuple):
        self._x_tile, self._y_tile = new_tile

    def __str__(self):
        return f"{self.color}{self.symbol}"

    def draw_piece(self, surface: pygame.Surface, w, board):
        margin = board.get_margin()
        surface.blit(self._figure_pic, (self._x_tile * w + margin[0], self._y_tile * w + margin[1]))

    def get_piece_data(self):
        return self._x_tile, self._y_tile, self._color, self._symbol

    @property
    def moves_count(self):
        return self._moves_count

    def upgrade_moves_count(self):
        self._moves_count += 1

    @property
    def color(self):
        return self._color

    @property
    def symbol(self):
        return self._symbol

    @property
    def tiles(self):
        return self._x_tile, self._y_tile

    @abstractmethod
    def get_possible_moves(self, field):
        pass


class King(Piece):  # ############# add castle
    def __init__(self, x_tile: int, y_tile: int, color: str):
        super().__init__(x_tile, y_tile, color, symbol="K")

    def get_possible_moves(self, field: list, last_move: tuple = None):
        possible_moves = []
        current_pos = self._x_tile, self._y_tile
        for direc in self._DIRECTIONS.values():
            option = optionx, optiony = tuple(map(sum, list(zip(direc, current_pos))))
            try:
                if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                    if field[optiony][optionx] == 0 or field[optiony][optionx].color != self.color:
                        possible_moves.append(option)
            except IndexError:
                pass

        # castle
        if self.moves_count == 0:
            # 0-0-0 castle
            if field[self._y_tile][0] != 0 and field[self._y_tile][0].moves_count == 0:
                empty = True
                for i in range(1, self._x_tile):
                    if field[self._y_tile][i] != 0:
                        empty = False
                        break
                if empty:
                    option = tuple(map(sum, list(zip(self._DIRECTIONS["W"], current_pos))))

                    next_option = tuple(map(sum, list(zip(self._DIRECTIONS["W"], option))))
                    # print(current_pos, self._DIRECTIONS["W"], option, next_option)

                    possible_moves.append(next_option)

            # 0-0 castle
            if field[self._y_tile][7] != 0 and field[self._y_tile][7].moves_count == 0:
                empty = True
                for i in range(self._x_tile + 1, 7):
                    if field[self._y_tile][i] != 0:
                        empty = False
                        break
                if empty:
                    option = tuple(map(sum, list(zip(self._DIRECTIONS["E"], current_pos))))

                    next_option = tuple(map(sum, list(zip(self._DIRECTIONS["E"], option))))
                    possible_moves.append(next_option)

        return possible_moves


class Pawn(Piece):  # ############# add weird capture and transformation
    def __init__(self, x_tile: int, y_tile: int, color: str):
        super().__init__(x_tile, y_tile, color, symbol="P")

    def get_possible_moves(self, field: list, last_move: tuple = None):
        possible_moves = []
        current_pos = self._x_tile, self._y_tile

        try:
            option = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS["N"], current_pos))))
            if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                if field[optiony][optionx] == 0:
                    possible_moves.append(option)

                    # first pawn move on 2 spaces
                    option_dbl = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS["N"], option))))
                    if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                        if field[optiony][optionx] == 0 and field[self._y_tile][self._x_tile].moves_count == 0:
                            possible_moves.append(option_dbl)
        except IndexError:
            pass

        try:
            option = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS["NW"], current_pos))))
            near_option = near_optionx, near_optiony = tuple(map(sum, list(zip(self._DIRECTIONS["W"], current_pos))))
            if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                if field[optiony][optionx] != 0 and field[optiony][optionx].color != self.color:
                    possible_moves.append(option)

            if 0 <= near_optionx < len(field[0]) and 0 <= near_optiony < len(field):
                if field[near_optiony][near_optionx] != 0 and \
                        field[near_optiony][near_optionx].color != self.color and \
                        field[near_optiony][near_optionx].moves_count == 1 and \
                        near_optiony in [3, len(field) - 3] and \
                        field[near_optiony][near_optionx].symbol == "P" and \
                        near_option == last_move:
                    possible_moves.append(option)
        except IndexError:
            pass

        try:
            option = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS["NE"], current_pos))))
            near_option = near_optionx, near_optiony = tuple(map(sum, list(zip(self._DIRECTIONS["E"], current_pos))))

            if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                if field[optiony][optionx] != 0 and field[optiony][optionx].color != self.color:
                    possible_moves.append(option)
            if 0 <= near_optionx < len(field[0]) and 0 <= near_optiony < len(field):
                if field[near_optiony][near_optionx] != 0 and \
                        field[near_optiony][near_optionx].color != self.color and \
                        field[near_optiony][near_optionx].moves_count == 1 and \
                        near_optiony in [3, len(field) - 3] and \
                        field[near_optiony][near_optionx].symbol == "P" and \
                        near_option == last_move:
                    possible_moves.append(option)
        except IndexError:
            pass

        return possible_moves


class Rook(Piece):
    def __init__(self, x_tile: int, y_tile: int, color: str):
        super().__init__(x_tile, y_tile, color, symbol="R")

    def get_possible_moves(self, field: list, last_move: tuple = None):
        possible_moves = []

        for direc in self._DIRECTIONS:
            if len(direc) == 1:
                current_pos = None
                while True:
                    if not current_pos:
                        current_pos = self._x_tile, self._y_tile

                    option = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS[direc], current_pos))))

                    try:
                        if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                            if field[optiony][optionx] == 0:
                                possible_moves.append(option)
                                current_pos = option
                                continue
                            elif field[optiony][optionx].color != self.color:
                                possible_moves.append(option)
                                break
                            else:
                                break
                        else:
                            break
                    except IndexError:
                        break

        return possible_moves


class Bishop(Piece):
    def __init__(self, x_tile: int, y_tile: int, color: str):
        super().__init__(x_tile, y_tile, color, symbol="B")

    def get_possible_moves(self, field: list, last_move: tuple = None):
        possible_moves = []

        for direc in self._DIRECTIONS:
            if len(direc) == 2:
                current_pos = None
                while True:
                    if not current_pos:
                        current_pos = self._x_tile, self._y_tile

                    option = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS[direc], current_pos))))

                    try:
                        if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                            if field[optiony][optionx] == 0:
                                possible_moves.append(option)
                                current_pos = option
                                continue
                            elif field[optiony][optionx].color != self.color:
                                possible_moves.append(option)
                                break
                            else:
                                break
                        else:
                            break
                    except IndexError:
                        break

        return possible_moves


class Queen(Piece):
    def __init__(self, x_tile: int, y_tile: int, color: str):
        super().__init__(x_tile, y_tile, color, symbol="Q")

    def get_possible_moves(self, field: list, last_move: tuple = None):
        possible_moves = []

        for direc in self._DIRECTIONS:
            current_pos = None
            while True:
                if not current_pos:
                    current_pos = self._x_tile, self._y_tile

                option = optionx, optiony = tuple(map(sum, list(zip(self._DIRECTIONS[direc], current_pos))))

                try:
                    if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                        if field[optiony][optionx] == 0:
                            possible_moves.append(option)
                            current_pos = option
                            continue
                        elif field[optiony][optionx].color != self.color:
                            possible_moves.append(option)
                            break
                        else:
                            break
                    else:
                        break
                except IndexError:
                    break

        return possible_moves


class Knight(Piece):
    def __init__(self, x_tile: int, y_tile: int, color: str):
        super().__init__(x_tile, y_tile, color, symbol="N")
        self._DIRECTIONS = [
            (-1, -2),
            (1, -2),
            (2, -1),
            (2, 1),
            (-1, 2),
            (1, 2),
            (-2, -1),
            (-2, 1),
        ]  # only for knight

    def get_possible_moves(self, field: list, last_move: tuple = None):
        possible_moves = []
        current_pos = self._x_tile, self._y_tile
        for direc in self._DIRECTIONS:
            option = optionx, optiony = tuple(map(sum, list(zip(direc, current_pos))))
            try:
                if 0 <= optionx < len(field[0]) and 0 <= optiony < len(field):
                    if field[optiony][optionx] == 0 or field[optiony][optionx].color != self.color:
                        possible_moves.append(option)
            except IndexError:
                pass
        return possible_moves


class ChessBoard(RectField):

    def __init__(self, x: float, y: float, cell_size: int, surface: pygame.Surface,
                 field: list,
                 black_tile_color: tuple = (120, 20, 20),
                 white_tile_color: tuple = (200, 200, 200)):

        super().__init__(x, y,
                         width=1 + cell_size * len(field[0]), height=1 + cell_size * len(field),
                         surface=surface,
                         color=(80, 0, 40))
        self._cell_size = cell_size
        self._board_color = black_tile_color
        self._white_tile_color = white_tile_color
        self._black_tile_color = black_tile_color
        self._active_tile_color = (200, 200, 0)
        self._active_tile = None
        self._possible_moves = []
        self._surface = surface
        self._field = field
        self._last_move_from = None
        self._last_move_to = None
        self._is_check = False

    def get_margin(self):
        return self._x, self._y

    def set_is_check(self, king_in_danger: tuple or False):
        self._is_check = king_in_danger

    def set_active_tile(self, active_tile: tuple or None):
        self._active_tile = active_tile

    def set_possible_moves(self, possible_moves: list):
        self._possible_moves = possible_moves

    def set_last_move(self, last_move: tuple):
        self._last_move_to = last_move

    def draw_board(self):
        # black \ white tiles
        for i, row in enumerate(self._field):
            for j, el in enumerate(row):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self._surface, self._white_tile_color,
                                     [self._x + (self._cell_size * j), self._y + (self._cell_size * i),
                                      self._cell_size, self._cell_size])
                elif (i + j) % 2 == 1:
                    pygame.draw.rect(self._surface, self._black_tile_color,
                                     [self._x + (self._cell_size * j), self._y + (self._cell_size * i),
                                      self._cell_size, self._cell_size])

        # checked King
        if self._is_check:
            font = pygame.font.Font("freesansbold.ttf", 32)
            check = font.render(f"Check", True, (255, 0, 0))
            self._surface.blit(check, (self._x + self._cell_size * 9, self._y + self._cell_size * 0))

            pygame.draw.rect(self._surface, (230, 20, 10),
                             [self._x + (self._cell_size * self._is_check[0] ), self._y +
                              (self._cell_size * self._is_check[1]),
                              self._cell_size, self._cell_size])

        # Picked piece
        if self._active_tile:
            pygame.draw.rect(self._surface, self._active_tile_color,
                             [
                                 self._x + (self._cell_size * self._active_tile[0]),
                                 self._y + (self._cell_size * self._active_tile[1]),
                                 self._cell_size,
                                 self._cell_size
                             ]
                             )

        # last move
        if self._last_move_from:
            pygame.draw.rect(self._surface, (0, 170, 10),
                             [
                                 self._x + (self._cell_size * self._last_move_to[0]),
                                 self._y + (self._cell_size * self._last_move_to[1]),
                                 self._cell_size,
                                 self._cell_size
                             ]
                             )

            pygame.draw.rect(self._surface, (0, 170, 10),
                             [
                                 self._x + (self._cell_size * self._last_move_from[0]),
                                 self._y + (self._cell_size * self._last_move_from[1]),
                                 self._cell_size,
                                 self._cell_size
                             ]
                             )

        # Options to move
        if self._possible_moves:
            for i in self._possible_moves:
                pygame.draw.rect(self._surface, self._active_tile_color,
                                 [
                                     self._x + (self._cell_size * i[0]),
                                     self._y + (self._cell_size * i[1]),
                                     self._cell_size,
                                     self._cell_size
                                 ]
                                 )

        # grid
        for hor in range(len(self._field) + 1):
            pygame.draw.line(self._surface, (0, 0, 0),
                             (0 + self._x, hor * self._cell_size + self._y),
                             (len(self._field[0]) * self._cell_size + self._x, hor * self._cell_size + self._y), 1)

        for ver in range(len(self._field[0]) + 1):
            pygame.draw.line(self._surface, (0, 0, 0),
                             (ver * self._cell_size + self._x, 0 + self._y),
                             (ver * self._cell_size + self._x, len(self._field) * self._cell_size + self._y), 1)

    def draw_transformation_options(self, color: str, surface: pygame.Surface) -> None:
        pieces = ["Q", "N", "B", "R"]
        for j in range(len(pieces)):
            pygame.draw.rect(self._surface, (255, 0, 0),
                             [self._x + (self._cell_size * 8),
                              self._y + (self._cell_size * (((len(self._field) - 4) / 2) + j)),
                              self._cell_size, self._cell_size])
            pygame.draw.rect(self._surface, (0, 0, 0),
                             [self._x + (self._cell_size * 8),
                              self._y + (self._cell_size * (((len(self._field) - 4) / 2) + j)),
                              self._cell_size, self._cell_size], 1)

            img = pygame.image.load(f"{color}{pieces[j]}.png")
            surface.blit(img, (
                self._x + (self._cell_size * 8), self._y + (self._cell_size * (((len(self._field) - 4) / 2) + j))))

    def make_field_prediction(self, destination_tile: tuple) -> list:
        x, y = self._active_tile
        temporary_field = [[0 for __ in range(len(self._field[0]))] for _ in
                           range(len(self._field))]  # copy of the field for returning to consideration
        destx, desty = destination_tile

        for i, row in enumerate(self._field):
            for j, el in enumerate(row):
                if self._field[i][j] != 0:
                    temporary_field[i][j] = self._field[i][j]

        temporary_field[desty][destx] = temporary_field[y][x]
        temporary_field[y][x] = 0

        return temporary_field

    def make_move(self, destination_tile: tuple) -> None:
        if destination_tile in self._possible_moves:
            x, y = self._active_tile
            destx, desty = destination_tile

            self._field[y][x].upgrade_moves_count()
            if self._field[y][x].symbol == "P" and destx != x and self._field[desty][destx] == 0:
                self._field[y][destx] = 0
            if self._field[y][x].symbol == "K" and abs(destx - x) == 2:
                if destx - x < 0:  # 0-0-0
                    self._field[y][x - 1] = self._field[y][0]
                    self._field[y][0] = 0
                    self._field[y][x - 1].set_new_tile((x - 1, y))

                if destx - x > 0:  # 0-0
                    self._field[y][x + 1] = self._field[y][7]
                    self._field[y][7] = 0
                    self._field[y][x + 1].set_new_tile((x + 1, y))

            self._field[desty][destx] = self._field[y][x]
            self._field[y][x] = 0

            self._field[desty][destx].set_new_tile((destx, desty))
            self._last_move_from = x, y
            # print(self._last_move_from)
            self._is_check = False

    def get_field(self):
        return self._field

    def set_field(self, field):
        self._field = field

    def get_board_coords(self) -> tuple:
        return self._x, self._y

    def get_tiles(self, event) -> tuple:
        """Return indexes of clicked tile (x, y)"""
        return (event.pos[0] - self.get_board_coords()[0]) // self._cell_size, \
               (event.pos[1] - self.get_board_coords()[0]) // self._cell_size

    def add_piece(self, piece: Piece):
        x, y, c, s = piece.get_piece_data()
        self._field[y][x] = piece
        # print(self._field)

    def draw_all_pieces(self):
        for i in self._field:
            for j in i:
                if j != 0:
                    j.draw_piece(self._surface, self._cell_size, self)
