import sys
import os

import pygame

from game import Game
from omok.enums import GameMode, GameStateEnum, TurnStateEnum
from omok.config import BOARD_SIZE
from agent import BaseAgent, HumanAgent

IMAGE_DIR = os.path.join(os.getcwd(), 'resources/images/')


class Board(object):
    def __init__(self, black_agent: BaseAgent, white_agent: BaseAgent):
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

        pygame.init()
        # image
        self.white_img = pygame.transform.scale(
            pygame.image.load(os.path.join(IMAGE_DIR, 'white.png')),
            self.grid_size
        )
        self.black_img = pygame.transform.scale(
            pygame.image.load(os.path.join(IMAGE_DIR, 'black.png')),
            self.grid_size
        )
        self.last_white_img = pygame.image.load(
            os.path.join(IMAGE_DIR, 'white_a.png')
        )
        self.last_black_img = pygame.image.load(
            os.path.join(IMAGE_DIR, 'black_a.png')
        )
        self.board_img = pygame.image.load(
            os.path.join(IMAGE_DIR, 'board.png')
        )
        self.font = pygame.font.Font('freesansbold.ttf', 14)
        self.point_pixels = [
            [
                (x * self.grid_size[0] + 25, y * self.grid_size[0] + 25)
                for y in range(BOARD_SIZE)
            ] for x in range(BOARD_SIZE)
        ]
        self.last_black_point = None
        self.last_white_point = None

        # game and agents
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.game = Game(self.black_agent, self.white_agent)
        self.human_agent_count = len(
            [agent for agent in [self.black_agent, self.white_agent] if isinstance(agent, HumanAgent)]
        )

    def initialize(self):
        self.count = 0
        if self.human_agent_count == 2:
            self.target_agent = self.black_agent
            self.next_target_agent = self.white_agent
        else:
            if isinstance(self.black_agent, HumanAgent):
                self.target_agent = self.black_agent
                self.next_target_agent = self.black_agent
            else:
                self.target_agent = self.white_agent
                self.next_target_agent = self.white_agent

    def change_agent(self):
        if self.human_agent_count == 2:
            self.target_agent, self.next_target_agent = self.next_target_agent, self.target_agent

    def draw_board(self):
        self.surface.blit(self.board_img, (0, 0))

    def draw_image(self, x, y, image):
        self.surface.blit(image, (x, y))

    def draw_number(self, x, y, color, number):
        self.make_text(self.font, str(number), color, None, x + 15, y + 15, 1)

    def get_point(self, pos):
        x = (pos[0] - 25) // 30
        y = (pos[1] - 25) // 30
        if (
            (x < 0 or y < 0 or x > 14 or y > 14)
            or (
                pos[0] < x * 30 + 32
                or pos[0] > x * 30 + 48
                or pos[1] < y * 30 + 32
                or pos[1] > y * 30 + 48
            )
            ):
            return None
        return x, y

    def draw_stone(self, pos):
        point =  self.get_point(pos)
        if point is None:
            return False

        x, y = point
        point_pixels = self.point_pixels[x][y]
        if self.game.current_turn == TurnStateEnum.BLACK:
            image = self.black_img
            last_image = self.last_black_img
            last_point = self.last_black_point
            self.last_black_point = point_pixels
        else:
            image = self.white_img
            last_image = self.last_white_img
            last_point = self.last_white_point
            self.last_white_point = point_pixels

        if last_point is not None:
            self.draw_image(last_point[0], last_point[1], image)
            self.draw_number(last_point[0], last_point[1], self.white, self.count)
        self.count += 1
        self.draw_image(point_pixels[0], point_pixels[1], last_image)
        self.draw_number(point_pixels[0], point_pixels[1], self.red, self.count)
        return True

    def set_menu(self):
        top, left = self.window_size[1] - 30, self.window_size[0] - 100
        self.new_menu = self.make_text(self.font, 'New Game', self.blue, None, top - 30, left)
        self.quit_menu = self.make_text(self.font, 'Quit Game', self.blue, None, top, left)
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
            rect.center = (top, left)
        else:    
            rect.topleft = (top, left)
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

    def start(self):
        self.initialize()
        self.surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Omok game")
        self.surface.fill(self.backgroud_color)
        self.draw_board()
        self.set_menu()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = event.pos
                    if pos[0] >= 25 and pos[0] <= 475 and pos[1] >= 25 and pos[1] <= 475:
                        if (
                            self.game.state == GameStateEnum.CONTINUE
                            and self.game.lock.acquire(block=False)
                        ):
                            self.target_agent.input_queue.put(pos)
                            self.game.lock.release()
                            success = self.draw_stone(pos)
                            if success:
                                self.game.lock.acquire()
                                if self.game.state != GameStateEnum.CONTINUE:
                                    self.show_message(f'Game Finished : {self.game.state.value}')
                                self.game.lock.release()
                                self.change_agent()
                    elif self.new_menu.collidepoint(pos):
                        self.restart()
                    # elif self.show_rect.collidepoint(pos):
                    #     self.show_hide(omok)
                    # elif self.undo_rect.collidepoint(pos):
                    #     omok.undo()
                    # elif self.uall_rect.collidepoint(pos):
                    #     omok.undo_all()
                    # elif self.redo_rect.collidepoint(pos):
                    #     omok.redo()
                    elif self.quit_menu.collidepoint(pos):
                        self.terminate()

            pygame.display.update()
            clock.tick(10)
            

