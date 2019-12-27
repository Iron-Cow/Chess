import pygame


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


class Piece(object):
    def __init__(self, x_tile: int, y_tile: int, color: str, symbol: str):
        self._symbol = symbol
        self._x_tile = x_tile
        self._y_tile = y_tile
        self._color = color
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self._figure_pic = self.font.render(f"{self._symbol}", True, (20, 200, 200))  # fix to picture

    def __str__(self):
        return f"{self.color}"

    def draw_piece(self, surface: pygame.Surface, w, board):
        margin = board.get_margin()
        surface.blit(self._figure_pic, ((self._x_tile + 0.25) * w + margin[0], (self._y_tile + 0.25) * w + margin[1]))

    def get_piece_data(self):
        return self._x_tile, self._y_tile, self._color, self._symbol

    @property
    def color(self):
        return self._color


class ChessBoard(RectField):

    def __init__(self, x: float, y: float, cell_size: int, surface: pygame.Surface,
                 field: list,
                 black_tile_color: tuple = (20, 20, 20),
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
        self._field = field

    def get_margin(self):
        return self._x, self._y

    def set_active_tile(self, active_tile: tuple or None):
        self._active_tile = active_tile

    def draw_board(self):
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
        if self._active_tile:
            pygame.draw.rect(self._surface, self._active_tile_color,
                             [
                                 self._x + (self._cell_size * self._active_tile[0]),
                                 self._y + (self._cell_size * self._active_tile[1]),
                                 self._cell_size,
                                 self._cell_size
                             ]
                             )

    def get_field(self):
        return self._field

    def get_board_coords(self) -> tuple:
        return self._x, self._y

    def get_tiles(self, event) -> tuple:
        """Return indexes of clicked tile (x, y)"""
        return (event.pos[0] - self.get_board_coords()[0]) // self._cell_size, \
               (event.pos[1] - self.get_board_coords()[0]) // self._cell_size

    def add_piece(self, piece: Piece):
        x, y, c, s = piece.get_piece_data()
        self._field[y][x] = piece
        print(self._field)

    def draw_all_pieces(self):
        for i in self._field:
            for j in i:
                if j != 0:
                    j.draw_piece(self._surface, self._cell_size, self)

# class GameWindow(RectField):
#     """Chess window for the game"""
#     def __init__(self, color, grid_color: tuple, game_cell: Cell, field: list):
#         """
#         :param color:
#         :param grid_color:
#         :param game_cell:
#         :param field: [8x8] list of lists
#         """
#         super().__init__(x=0, y=0,
#                          width=len(field[0])*game_cell.get_w(),
#                          height=len(field)*game_cell.get_w(),
#                          color=color)
#         self.__grid_color = grid_color
#         self.__game_cell = game_cell
#         self.__field = field
#
#     def draw_grid(self, surface):
#         # surface.fill(self._color)
#         for x, _ in enumerate(self.__field[0]):  # Vertical lines
#             pygame.draw.line(surface,
#                              self.__grid_color,
#                              (x * self.__game_cell.get_w(), 0),
#                              (x * self.__game_cell.get_w(), self._height),
#                              width=1
#                              )
#
#         for y, _ in enumerate(self.__field):  # Horizontal lines
#             pygame.draw.line(surface,
#                              self.__grid_color,
#                              (0, y * self.__game_cell.get_w()),
#                              (self._width, y * self.__game_cell.get_w()),
#                              width=1
#                              )
#
#         pygame.draw.line(surface,
#                          self.__grid_color,
#                          (self._width, 0),
#                          (self._width, self._height),
#                          width=1
#                              )
#
#         pygame.draw.line(surface,
#                          self.__grid_color,
#                          (0, self._height),
#                          (self._width, self._height,),
#                          width=1
#                          )
#
#     def draw_cells(self, surface):
#         for row in self.__field:
#             for cell in row:
#                 cell.draw(surface)
