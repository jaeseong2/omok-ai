import pygame
import sys

from game import Game

import config

class Board(object):
    def __init__(self, game: Game):
        # size
        self.window_size = (700, 500)
        self.board_size = (500, 500)
        self.grid_size = (30, 30)

        # color
        self.board_color = (204, 153, 000)
        self.backgroud_color = (128, 128, 128)
        self.black = (0, 0, 0)
        self.blue = (0, 50, 255)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 200, 0)

        # image
        self.white_img = pygame.transform.scale(
            pygame.image.load('images/white.png'),
            self.grid_size
        )
        self.black_img = pygame.transform.scale(
            pygame.image.load('images/black.png'),
            self.grid_size
        )
        self.last_white_img = pygame.image.load('images/white_a.png')
        self.last_black_img = pygame.image.load('images/black_a.png')
        self.board_img = pygame.image.load('images/board.png')

        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.game = game
        self.point_pixels = [
            [
                (x * self.grid_size + 25, y * self.grid_size + 25)
                for y in range(self.game.board_size)
            ] for x in range(self.game.board_size)
        ]
        self.last_black_point = None
        self.last_white_point = None

    def draw_board(self):
        self.surface.blit(self.board_img, (0, 0))

    def set_point(self, x, y, image):
        img = [self.black_img, self.white_img, self.last_b_img, self.last_w_img]
        self.surface.blit(img[img_index], (x, y))

    def set_number(self, x, y, stone, number):
        colors = [white, black, red, red]
        color = colors[stone]
        self.make_text(self.font, str(number), color, x + 15, y + 15, 'center')

    def set_menu(self):
        top, left = self.window_size[1] - 30, self.window_size[0] - 100
        self.new_rect = self.make_text(self.font, 'New Game', self.blue, None, top - 30, left)
        self.quit_rect = self.make_text(self.font, 'Quit Game', self.blue, None, top, left)
        # self.show_rect = self.make_text(self.font, 'Hide Number  ', self.blue, None, top - 60, left)
        # self.undo_rect = self.make_text(self.font, 'Undo', self.blue, None, top - 150, left)
        # self.uall_rect = self.make_text(self.font, 'Undo All', self.blue, None, top - 120, left)
        # self.redo_rect = self.make_text(self.font, 'Redo', self.blue, None, top - 90, left)

    def show_message(self, message):
        x = (self.window_size[0] + self.board_size[0]) // 2
        self.make_text(self.font, message, self.black, self.backgroud_color, 30, x, 1)

    def make_text(self, font, text, color, bgcolor, top, left, position=0):
        surf = font.render(text, False, color, bgcolor)
        rect = surf.get_rect()
        if position:
            rect.center = (left, top)
        else:    
            rect.topleft = (left, top)
        self.surface.blit(surf, rect)
        return rect

    # def undo(self):
    #     if not self.coords:
    #         return            
    #     self.draw_board()
    #     coord = self.coords.pop()
    #     self.redos.append(coord)
    #     self.draw_stone(coord, empty, -1)

    def restart(self):
        self.game.initialize()
        self.draw_board()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Omok game")
        self.surface.fill(self.backgroud_color)
        self.draw_board()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    pos = event.pos
                    if pos
                    elif self.new_rect.collidepoint(pos):
                        self.restart()
                    # elif self.show_rect.collidepoint(pos):
                    #     self.show_hide(omok)
                    # elif self.undo_rect.collidepoint(pos):
                    #     omok.undo()
                    # elif self.uall_rect.collidepoint(pos):
                    #     omok.undo_all()
                    # elif self.redo_rect.collidepoint(pos):
                    #     omok.redo()
                    elif self.quit_rect.collidepoint(pos):
                        self.terminate()

        if omok.is_gameover:
            return

