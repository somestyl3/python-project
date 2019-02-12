import pygame
import sys
from random import randrange as rand
from config import *


class TApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(100, 25)
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.limit = cell_size * cols
        self.background_grid = [[8 if x % 2 == y % 2 else 0 for x in range(cols)] for y in range(rows)]

        self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.next_stone = shapes[rand(len(shapes))]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = shapes[rand(len(shapes))]
        self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def display_msg(self, msg, topleft):
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255, 255, 255),
                    (0, 0, 0)),
                (x, y))
            y += 14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False,
                                                 (255, 255, 255), (0, 0, 0))

            msgimg_center_x, msgimg_center_y = msg_image.get_size()
            msgimg_center_x //= 2
            msgimg_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgimg_center_x,
                self.height // 2 - msgimg_center_y + i * 22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            cell_size,
                            (off_y + y) *
                            cell_size,
                            cell_size,
                            cell_size), 0)

    def add_cl_lines(self, n):
        score = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += score[n] * self.level
        if self.lines >= self.level * 6:
            self.level += 1
            delay = 1000 - 50 * (self.level - 1)
            delay = 100 if delay < 100 else delay
            pygame.time.set_timer(pygame.USEREVENT + 1, delay)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self):
        self.center_msg('Exiting...')
        pygame.display.update()
        sys.exit()

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join(
                    self.board,
                    self.stone,
                    (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(
                                self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def instant_drop(self):
        if not self.gameover and not self.paused:
            while not self.drop(True):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': lambda: self.drop(True),
            'UP': self.rotate_stone,
            'p': self.pause,
            'SPACE': self.start_game,
            'RETURN': self.instant_drop
        }

        self.gameover = False
        self.paused = False

        clock = pygame.time.Clock()
        while 1:
            self.screen.fill((0, 0, 0))
            if self.gameover:
                self.center_msg('''Game Over!\nYour score: %d Press space to continue''' % self.score)
            else:
                if self.paused:
                    self.center_msg('Paused')
                else:
                    pygame.draw.line(self.screen,
                                     (255, 255, 255),
                                     (self.limit + 1, 0),
                                     (self.limit + 1, self.height - 1))
                    self.display_msg('Next:', (
                        self.limit + cell_size,
                        2))
                    self.display_msg('Score: %d\n\nLevel: %d\
                    \nLines: %d' % (self.score, self.level, self.lines),
                                     (self.limit + cell_size, cell_size * 5))
                    self.draw_matrix(self.background_grid, (0, 0))
                    self.draw_matrix(self.board, (0, 0))
                    self.draw_matrix(self.stone,
                                     (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone,
                                     (cols + 1, 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval('pygame.K_' + key):
                            key_actions[key]()

            clock.tick(maxfps)
