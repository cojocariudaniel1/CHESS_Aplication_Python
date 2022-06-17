import pygame as pg
import logging
import copy
import numpy as np
from manimlib import *

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
initiate_matrix = [
    [-50, -30, -40, -9, -10, -41, -31, -51],
    [-11, -12, -13, -14, -15, -16, -17, -18],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [11, 12, 13, 14, 15, 16, 17, 18],
    [50, 30, 40, 9, 10, 41, 31, 51]
]

initiate_matrix1 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 12, 0, 14, 0, 0, 0, 0],
    [50, 0, 0, 0, 0, 0, -50, 0],
    [0, 16, 0, 0, 0, 0, 0, 0],
    [51, 0, 0, 0, 0, 0, 0, 0],
    [14, 13, 0, 0, 0, 0, 10, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 11, 0, 0, 0, 0, 0]
]

post_matrix = [
    [-50, -30, -40, -9, -10, -41, -31, -51],
    [-11, -12, -13, -14, -15, -16, -17, -18],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [11, 12, 13, 14, 15, 16, 17, 18],
    [50, 30, 40, 9, 10, 41, 31, 51]
]

initiate_matrix3 = [
    [-50, 0, -40, -9, 0, -51, 0, -10],
    [-11, -12, 0, -30, 0, -16, -17, -18],
    [0, 0, -13, 0, -15, -31, 0, 0],
    [0, 0, 0, -14, 0, 0, 40, 0],
    [0, 0, 13, 14, 0, 0, 0, 0],
    [0, 9, -41, 41, 15, 31, 0, 0],
    [11, 12, 0, 0, 0, 16, 17, 18],
    [50, 0, 0, 0, 0, 51, 10, 0]
]

clean_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]


def chess_pieces_image(image):
    img = pg.image.load(f"img/{image}.png")
    return pg.transform.scale(img, (80, 80))


def get_poisition(id_elm):
    for y in initiate_matrix:
        index_y = initiate_matrix.index(y)
        for x in y:
            index_x = y.index(x)
            if index_x == id_elm:
                return index_x, index_y


def p_multx(x):
    pos_x = x * 100

    return pos_x


def p_multy(y):
    pos_y = y * 100

    return pos_y


class ChessPieces(pg.sprite.Sprite):
    def __init__(self, id_pieces, image, screen, make_move=False):
        pg.sprite.Sprite.__init__(self)
        self.id = id_pieces
        self.image = image
        self.screen = screen
        self.rect = pg.image.load(f'img/{image}.png').get_rect()
        self.x_pos = None
        self.y_pos = None
        self.make_move = make_move
        self.moves = []
        self.color = (50, 0, 50)
        self.possible_moves = []
        self.enemy_moves = []
        self.cach_enemy_moves = []
        self.sah_count = 0
        self.sah_moves = []
        self.sah_bool = False

    def update_pieces(self):
        for y in initiate_matrix:
            index_y = initiate_matrix.index(y)
            for x in y:
                index_x = y.index(x)
                if x == self.id:
                    self.screen.blit(chess_pieces_image(self.image), (p_multx(index_x), p_multy(index_y)))
                    self.x_pos = index_x
                    self.y_pos = index_y

                    # if x == -14:
                    #     print( p_multx(index_x), p_multy(index_y) + 7)

    def append_in_possible_moves(self, k):
        if k not in self.moves:
            self.moves.append(k)

    def check_for_pin(self, id_pieces):
        print('check for pin')
        matrix_cach = copy.deepcopy(initiate_matrix)

        king_pos = self.king_position()
        for y in matrix_cach:
            index_y = matrix_cach.index(y)
            for x in y:
                index_x = y.index(x)
                if x == id_pieces:
                    matrix_cach[index_y][index_x] = 0

        print('cach matrix')
        for i in matrix_cach:
            print(i)

        print('initiate matrixaaaaaaaaaaaaaaaaaaaaaa')
        for j in initiate_matrix:
            print(j)

        self.enemy_possible_moves(king_pos, matrix_cach)
        if self.sah_count > 0:
            self.sah_count = 0
            return True

    def pion_draw_rect(self):
        self.moves.clear()
        self.sah_moves.clear()
        if not self.my_possible_moves(self.id):
            try:
                if self.id in [-11, -12, -13, -14, -15, -16, -17, -18] and self.make_move:
                    tempx = self.x_pos
                    tempy = self.y_pos
                    if initiate_matrix[self.y_pos + 1][self.x_pos] == 0:
                        if self.y_pos == 1:
                            y = 0
                            while y <= 1:
                                if initiate_matrix[self.y_pos + 1][self.x_pos] == 0:
                                    pg.draw.circle(self.screen, self.color,
                                                   (p_multx(self.x_pos) + 50, p_multy(self.y_pos) + 150),
                                                   15)
                                    k = (self.y_pos + 1, self.x_pos)
                                    self.append_in_possible_moves(k)
                                    self.y_pos += 1
                                y += 1

                            self.reset_coord(tempy, tempx)
                        else:
                            if initiate_matrix[self.y_pos + 1][self.x_pos] == 0:
                                pg.draw.circle(self.screen, self.color,
                                               (p_multx(self.x_pos) + 50, p_multy(self.y_pos) + 150),
                                               15)
                                if 0 == initiate_matrix[self.y_pos + 1][self.x_pos]:
                                    k = (self.y_pos + 1, self.x_pos)
                                    self.append_in_possible_moves(k)

                    if initiate_matrix[self.y_pos + 1][self.x_pos - 1] > 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)
                        k = (self.y_pos + 1, self.x_pos - 1)
                        self.append_in_possible_moves(k)

                    if initiate_matrix[self.y_pos + 1][self.x_pos + 1] > 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)
                        k = (self.y_pos + 1, self.x_pos + 1)
                        self.append_in_possible_moves(k)


            except Exception as e:
                pass
                # pg.draw.circle(self.screen, (232,100,50), (525, 250), 15)

            if self.id in [-30, -31] and self.make_move:
                if self.x_pos + 1 <= 7 and self.y_pos + 2 <= 7 and initiate_matrix[self.y_pos + 2][self.x_pos + 1] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) + 50),
                                   15)
                    k = (self.y_pos + 2, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 1 >= 0 and self.y_pos + 2 <= 7 and initiate_matrix[self.y_pos + 2][
                    self.x_pos + -1] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) + 50),
                                   15)
                    k = (self.y_pos + 2, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 2 >= 0 and self.y_pos + 1 <= 7 and initiate_matrix[self.y_pos + 1][self.x_pos - 2] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 2) + 50, p_multy(self.y_pos + 1) + 50),
                                   15)
                    k = (self.y_pos + 1, self.x_pos - 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos + 2 <= 7 and self.y_pos + 1 <= 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 2] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 2) + 50, p_multy(self.y_pos + 1) + 50),
                                   15)
                    k = (self.y_pos + 1, self.x_pos + 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos + 2 <= 7 and self.y_pos - 1 >= 0 and initiate_matrix[self.y_pos - 1][self.x_pos + 2] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 2) + 50, p_multy(self.y_pos - 1) + 50),
                                   15)
                    k = (self.y_pos - 1, self.x_pos + 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 2 >= 0 and self.y_pos - 1 >= 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 2] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 2) + 50, p_multy(self.y_pos - 1) + 50),
                                   15)
                    k = (self.y_pos - 1, self.x_pos - 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos + 1 <= 7 and self.y_pos - 2 >= 0 and initiate_matrix[self.y_pos - 2][self.x_pos + 1] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos - 2) + 50),
                                   15)
                    k = (self.y_pos - 2, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 1 >= 0 and self.y_pos - 2 >= 0 and initiate_matrix[self.y_pos - 2][self.x_pos - 1] >= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos - 2) + 50),
                                   15)
                    k = (self.y_pos - 2, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

            # white knight
            if self.id in [30, 31] and self.make_move:
                if self.x_pos + 1 <= 7 and self.y_pos + 2 <= 7 and initiate_matrix[self.y_pos + 2][self.x_pos + 1] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) + 50),
                                   15)
                    k = (self.y_pos + 2, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 1 >= 0 and self.y_pos + 2 <= 7 and initiate_matrix[self.y_pos + 2][
                    self.x_pos + -1] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) + 50),
                                   15)
                    k = (self.y_pos + 2, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 2 >= 0 and self.y_pos + 1 <= 7 and initiate_matrix[self.y_pos + 1][self.x_pos - 2] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 2) + 50, p_multy(self.y_pos + 1) + 50),
                                   15)
                    k = (self.y_pos + 1, self.x_pos - 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos + 2 <= 7 and self.y_pos + 1 <= 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 2] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 2) + 50, p_multy(self.y_pos + 1) + 50),
                                   15)
                    k = (self.y_pos + 1, self.x_pos + 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos + 2 <= 7 and self.y_pos - 1 >= 0 and initiate_matrix[self.y_pos - 1][self.x_pos + 2] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 2) + 50, p_multy(self.y_pos - 1) + 50),
                                   15)
                    k = (self.y_pos - 1, self.x_pos + 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 2 >= 0 and self.y_pos - 1 >= 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 2] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 2) + 50, p_multy(self.y_pos - 1) + 50),
                                   15)
                    k = (self.y_pos - 1, self.x_pos - 2)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos + 1 <= 7 and self.y_pos - 2 >= 0 and initiate_matrix[self.y_pos - 2][self.x_pos + 1] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos - 2) + 50),
                                   15)
                    k = (self.y_pos - 2, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                if self.x_pos - 1 >= 0 and self.y_pos - 2 >= 0 and initiate_matrix[self.y_pos - 2][self.x_pos - 1] <= 0:
                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos - 2) + 50),
                                   15)
                    k = (self.y_pos - 2, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

            if self.id in [11, 12, 13, 14, 15, 16, 17, 18] and self.make_move:
                tempx = self.x_pos
                tempy = self.y_pos
                # pg.draw.rect(self.screen, (32, 32, 70), (p_multx(self.x_pos), p_multy(self.y_pos + 1), 50, 50)
                # self.check_for_sah()
                if initiate_matrix[self.y_pos - 1][self.x_pos] == 0:
                    if self.y_pos == 6:
                        y = 0
                        while y <= 1:
                            if 0 == initiate_matrix[self.y_pos - 1][self.x_pos]:
                                pg.draw.circle(self.screen, self.color,
                                               (p_multx(self.x_pos) + 50, p_multy(self.y_pos) - 50),
                                               15)
                                j = (self.y_pos - 1, self.x_pos)
                                self.append_in_possible_moves(j)
                                self.y_pos -= 1
                            y += 1
                        self.reset_coord(tempy, tempx)
                    else:
                        pg.draw.circle(self.screen, self.color, (p_multx(self.x_pos) + 50, p_multy(self.y_pos) - 50),
                                       15)
                        if 0 == initiate_matrix[self.y_pos - 1][self.x_pos]:
                            k = (self.y_pos - 1, self.x_pos)
                            self.append_in_possible_moves(k)

                if initiate_matrix[self.y_pos - 1][self.x_pos - 1] < 0:
                    pg.draw.circle(self.screen, self.color, (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos) - 50),
                                   15)
                    k = (self.y_pos - 1, self.x_pos - 1)
                    self.append_in_possible_moves(k)

                try:
                    if initiate_matrix[self.y_pos - 1][self.x_pos + 1] < 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos) - 50),
                                       15)
                        k = (self.y_pos - 1, self.x_pos + 1)
                        self.append_in_possible_moves(k)
                except:
                    pass

            ########################################################################

            if self.id in [40, 41] and self.make_move:  # bishooop
                tempx = self.x_pos
                tempy = self.y_pos
                self.reset_coord(tempy, tempx)
                while True:  # dreapta jos
                    if self.y_pos < 7 and self.x_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                check_bool = True
                self.reset_coord(tempy, tempx)
                while True:  # stanga sus
                    if self.y_pos > 0 and self.x_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # Dreapta sus
                    if self.y_pos >= 0 and self.x_pos < 7 and initiate_matrix[self.y_pos - 1][self.x_pos + 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos) - 50),
                                       15)
                        k = (self.y_pos - 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sganga jos
                    if self.y_pos < 7 and self.x_pos >= 0 and initiate_matrix[self.y_pos + 1][self.x_pos - 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

            if self.id in [-40, -41] and self.make_move:  # bishooop
                tempx = self.x_pos
                tempy = self.y_pos
                self.reset_coord(tempy, tempx)
                while True:  # dreapta jos
                    if self.y_pos < 7 and self.x_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                check_bool = True
                self.reset_coord(tempy, tempx)
                while True:  # stanga sus
                    if self.y_pos > 0 and self.x_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # Dreapta sus

                    if self.y_pos > 0 and self.x_pos < 7 and initiate_matrix[self.y_pos - 1][self.x_pos + 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos) - 50),
                                       15)
                        k = (self.y_pos - 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sganga jos
                    if self.y_pos < 7 and self.x_pos >= 0 and initiate_matrix[self.y_pos + 1][self.x_pos - 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

            if self.id in [50, 51] and self.make_move:  # rock
                if not self.check_for_pin(self.id):
                    tempx = self.x_pos
                    tempy = self.y_pos
                    self.reset_coord(tempy, tempx)
                    while True:  # dreapta
                        if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] <= 0:

                            k = (self.y_pos, self.x_pos + 1)
                            if k not in self.moves:
                                self.moves.append(k)

                            pg.draw.circle(self.screen, self.color,
                                           (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 1) - 50),
                                           15)

                            self.x_pos += 1
                            if initiate_matrix[self.y_pos][self.x_pos] < 0:
                                break
                        else:
                            break
                    self.reset_coord(tempy, tempx)
                    while True:  # stanga
                        if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] <= 0:
                            pg.draw.circle(self.screen, self.color,
                                           (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 1) - 50),
                                           15)

                            k = (self.y_pos, self.x_pos - 1)
                            if k not in self.moves:
                                self.moves.append(k)

                            self.x_pos -= 1
                            if initiate_matrix[self.y_pos][self.x_pos] < 0:
                                break
                        else:
                            break
                    self.reset_coord(tempy, tempx)
                    while True:  # sus
                        if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] <= 0:
                            pg.draw.circle(self.screen, self.color,
                                           (p_multx(self.x_pos) + 50, p_multy(self.y_pos) - 50),
                                           15)

                            k = (self.y_pos - 1, self.x_pos)
                            if k not in self.moves:
                                self.moves.append(k)

                            self.y_pos -= 1
                            if initiate_matrix[self.y_pos][self.x_pos] < 0:
                                break
                        else:
                            break
                    self.reset_coord(tempy, tempx)
                    while True:  # jos
                        if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] <= 0:
                            pg.draw.circle(self.screen, self.color,
                                           (p_multx(self.x_pos) + 50, p_multy(self.y_pos + 2) - 50),
                                           15)

                            k = (self.y_pos + 1, self.x_pos)
                            if k not in self.moves:
                                self.moves.append(k)

                            self.y_pos += 1
                            if initiate_matrix[self.y_pos][self.x_pos] < 0:
                                break
                        else:
                            break
                    self.reset_coord(tempy, tempx)
                else:
                    self.moves_if_in_sah()

            if self.id in [-50, -51] and self.make_move:  # bishooop
                tempx = self.x_pos
                tempy = self.y_pos
                self.reset_coord(tempy, tempx)
                while True:  # dreapta
                    if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 1) - 50),
                                       15)

                        k = (self.y_pos, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # stanga
                    if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 1) - 50),
                                       15)

                        k = (self.y_pos, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sus
                    if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # jos
                    if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

            if self.id in [9] and self.make_move:
                tempx = self.x_pos
                tempy = self.y_pos
                self.reset_coord(tempy, tempx)
                while True:  # dreapta
                    if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 1) - 50),
                                       15)

                        k = (self.y_pos, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # stanga
                    if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 1) - 50),
                                       15)

                        k = (self.y_pos, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sus
                    if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # jos
                    if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

                while True:  # dreapta jos
                    if self.y_pos < 7 and self.x_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                check_bool = True
                self.reset_coord(tempy, tempx)
                while True:  # stanga sus
                    if self.y_pos > 0 and self.x_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # Dreapta sus
                    if self.y_pos >= 0 and self.x_pos < 7 and initiate_matrix[self.y_pos - 1][self.x_pos + 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos) - 50),
                                       15)
                        k = (self.y_pos - 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sganga jos
                    if self.y_pos < 7 and self.x_pos >= 0 and initiate_matrix[self.y_pos + 1][self.x_pos - 1] <= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

            if self.id in [-9, -90, -91] and self.make_move:  # queen
                tempx = self.x_pos
                tempy = self.y_pos
                self.reset_coord(tempy, tempx)
                while True:  # dreapta jos
                    if self.y_pos < 7 and self.x_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                check_bool = True
                self.reset_coord(tempy, tempx)
                while True:  # stanga sus
                    if self.y_pos > 0 and self.x_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)
                        self.x_pos -= 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # Dreapta sus
                    if self.y_pos >= 0 and self.x_pos < 7 and initiate_matrix[self.y_pos - 1][self.x_pos + 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos) - 50),
                                       15)
                        k = (self.y_pos - 1, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] < 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sganga jos
                    if self.y_pos < 7 and self.x_pos >= 0 and initiate_matrix[self.y_pos + 1][self.x_pos - 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

                while True:  # dreapta
                    if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos + 1) + 50, p_multy(self.y_pos + 1) - 50),
                                       15)

                        k = (self.y_pos, self.x_pos + 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # stanga
                    if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos - 1) + 50, p_multy(self.y_pos + 1) - 50),
                                       15)

                        k = (self.y_pos, self.x_pos - 1)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.x_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # sus
                    if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos) + 50, p_multy(self.y_pos) - 50),
                                       15)

                        k = (self.y_pos - 1, self.x_pos)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.y_pos -= 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)
                while True:  # jos
                    if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] >= 0:
                        pg.draw.circle(self.screen, self.color,
                                       (p_multx(self.x_pos) + 50, p_multy(self.y_pos + 2) - 50),
                                       15)

                        k = (self.y_pos + 1, self.x_pos)
                        if k not in self.moves:
                            self.moves.append(k)

                        self.y_pos += 1
                        if initiate_matrix[self.y_pos][self.x_pos] > 0:
                            break
                    else:
                        break
                self.reset_coord(tempy, tempx)

            if self.id in [10] and self.make_move:
                tempx = self.x_pos
                tempy = self.y_pos
                self.reset_coord(tempy, tempx)
                if self.x_pos > 7 and initiate_matrix[self.y_pos][self.x_pos] <= 0:
                    pass
        else:
            self.moves.clear()
            self.moves_if_in_sah()

    def moves_if_in_sah(self):
        print('use this')
        self.sah_bool = True
        tempx = self.x_pos
        tempy = self.y_pos
        self.reset_coord(tempy, tempx)

        if self.id in [9]:
            tempx = self.x_pos
            tempy = self.y_pos
            self.reset_coord(tempy, tempx)
            while True:  # dreapta
                if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] <= 0:
                    k = (self.y_pos, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # stanga
                if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] <= 0:
                    k = (self.y_pos, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # sus
                if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] <= 0:
                    k = (self.y_pos - 1, self.x_pos)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # jos
                if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] <= 0:
                    k = (self.y_pos + 1, self.x_pos)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)

            while True:  # dreapta jos
                if self.y_pos < 7 and self.x_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 1] <= 0:

                    k = (self.y_pos + 1, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos += 1
                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            check_bool = True
            self.reset_coord(tempy, tempx)
            while True:  # stanga sus
                if self.y_pos > 0 and self.x_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 1] <= 0:
                    k = (self.y_pos - 1, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos -= 1
                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # Dreapta sus
                if self.y_pos >= 0 and self.x_pos < 7 and initiate_matrix[self.y_pos - 1][self.x_pos + 1] <= 0:
                    k = (self.y_pos - 1, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos += 1
                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # sganga jos
                if self.y_pos < 7 and self.x_pos >= 0 and initiate_matrix[self.y_pos + 1][self.x_pos - 1] <= 0:
                    k = (self.y_pos + 1, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos -= 1
                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)

        if self.id in [-9] and self.make_move:  # queen
            tempx = self.x_pos
            tempy = self.y_pos
            self.reset_coord(tempy, tempx)
            while True:  # dreapta jos
                if self.y_pos < 7 and self.x_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos + 1] >= 0:
                    k = (self.y_pos + 1, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos += 1
                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] > 0:
                        break
                else:
                    break
            check_bool = True
            self.reset_coord(tempy, tempx)
            while True:  # stanga sus
                if self.y_pos > 0 and self.x_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos - 1] >= 0:
                    k = (self.y_pos - 1, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)
                    self.x_pos -= 1
                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # Dreapta sus
                if self.y_pos >= 0 and self.x_pos < 7 and initiate_matrix[self.y_pos - 1][self.x_pos + 1] >= 0:
                    k = (self.y_pos - 1, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos += 1
                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # sganga jos
                if self.y_pos < 7 and self.x_pos >= 0 and initiate_matrix[self.y_pos + 1][self.x_pos - 1] >= 0:
                    k = (self.y_pos + 1, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos -= 1
                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] > 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)

            while True:  # dreapta
                if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] >= 0:
                    k = (self.y_pos, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] > 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # stanga
                if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] >= 0:
                    k = (self.y_pos, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] > 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # sus
                if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] >= 0:

                    k = (self.y_pos - 1, self.x_pos)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] > 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # jos
                if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] >= 0:
                    k = (self.y_pos + 1, self.x_pos)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] > 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)

        if self.id in [50, 51]:
            while True:  # dreapta
                if self.x_pos < 7 and initiate_matrix[self.y_pos][self.x_pos + 1] <= 0:

                    k = (self.y_pos, self.x_pos + 1)
                    if k not in self.moves:
                        self.moves.append(k)
                    self.x_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # stanga
                if self.x_pos > 0 and initiate_matrix[self.y_pos][self.x_pos - 1] <= 0:

                    k = (self.y_pos, self.x_pos - 1)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.x_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # sus
                if self.y_pos > 0 and initiate_matrix[self.y_pos - 1][self.x_pos] <= 0:

                    k = (self.y_pos - 1, self.x_pos)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.y_pos -= 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            while True:  # jos
                if self.y_pos < 7 and initiate_matrix[self.y_pos + 1][self.x_pos] <= 0:

                    k = (self.y_pos + 1, self.x_pos)
                    if k not in self.moves:
                        self.moves.append(k)

                    self.y_pos += 1
                    if initiate_matrix[self.y_pos][self.x_pos] < 0:
                        break
                else:
                    break
            self.reset_coord(tempy, tempx)
            print(f'self.moves = : {self.moves}')
            for i in self.moves:
                if i in self.cach_enemy_moves:
                    # k = (i[] + 1, self.x_pos)
                    # if k not in self.moves:
                    #     self.moves.append(k)

                    pg.draw.circle(self.screen, self.color,
                                   (p_multx(i[1]) + 50, p_multy(i[0]) + 50),
                                   15)
                    k = (i[0], i[1])
                    if k not in self.sah_moves:
                        self.sah_moves.append(k)
            print(f"sah bool: {self.sah_bool}, sah_moves: {self.sah_moves}, moves: {self.moves}")

    def my_possible_moves(self, id_piece):
        for y in initiate_matrix:
            index_y = initiate_matrix.index(y)
            for x in y:
                index_x = y.index(x)
                tempy = index_y
                tempx = index_x
                if id_piece == initiate_matrix[index_y][index_x]:
                    print("id piesa posibilitati:", id_piece)

                    if id_piece in [11, 12, 13, 14, 15, 16, 17, 18]:
                        tempx = index_x
                        tempy = index_y
                        if initiate_matrix[index_y - 1][index_x] == 0:
                            if index_y == 6:
                                p = 0
                                while p <= 1:
                                    if 0 == initiate_matrix[index_y - 1][index_x]:
                                        j = (index_y - 1, index_x)
                                        self.possible_moves.append(j)
                                        index_y -= 1
                                    p += 1
                                index_y = tempy
                                index_x = tempx

                            else:
                                if 0 == initiate_matrix[index_y - 1][index_x]:
                                    k = (index_y - 1, index_x)
                                    self.possible_moves.append(k)

                        if initiate_matrix[index_y - 1][index_x - 1] < 0:
                            k = (index_y - 1, index_x - 1)
                            self.possible_moves.append(k)

                        try:
                            if initiate_matrix[index_y - 1][index_x + 1] < 0:
                                k = (index_y - 1, index_x + 1)
                                self.possible_moves.append(k)

                        except:
                            pass
                        index_y = tempy
                        index_x = tempx

                    if id_piece in [-11, -12, -13, -14, -15, -16, -17, -18]:

                        tempx = index_x
                        tempy = index_y
                        if initiate_matrix[index_y + 1][index_x] == 0:
                            if index_y == 1:
                                p = 0
                                while p <= 1:
                                    if initiate_matrix[index_y + 1][index_x] == 0:
                                        k = (index_y + 1, index_x)
                                        self.possible_moves.append(k)
                                        index_y += 1
                                    p += 1

                                index_y = tempy
                                index_x = tempx

                            else:
                                if initiate_matrix[index_y + 1][index_x] == 0:
                                    if 0 == initiate_matrix[index_y + 1][index_x]:
                                        k = (index_y + 1, index_x)
                                        self.possible_moves.append(k)
                        if index_y < 7 and index_x > 0:
                            if initiate_matrix[index_y + 1][index_x - 1] > 0:
                                k = (index_y + 1, index_x - 1)
                                self.possible_moves.append(k)

                        if index_y < 7 and index_x < 7:
                            if initiate_matrix[index_y + 1][index_x + 1] > 0:
                                k = (index_y + 1, index_x + 1)
                                self.possible_moves.append(k)
                            index_y = tempy
                            index_x = tempx

                    if id_piece in [50, 51]:
                        while True:  # dreapta
                            if index_x < 7 and initiate_matrix[index_y][index_x + 1] <= 0:

                                k = (index_y, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break

                        index_y = tempy
                        index_x = tempx

                        while True:  # sus
                            if index_y > 0 and initiate_matrix[index_y - 1][index_x] <= 0:

                                k = (index_y - 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    index_y = tempy
                                    index_x = tempx
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        while True:  # jos
                            if index_y < 7 and initiate_matrix[index_y + 1][index_x] <= 0:

                                k = (index_y + 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        while True:  # stanga
                            if index_x > 0 and initiate_matrix[index_y][index_x - 1] <= 0:

                                k = (index_y, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                    if id_piece in [-50, -51]:  # bishooop
                        tempx = index_x
                        tempy = index_y
                        index_y = tempy
                        index_x = tempx
                        while True:  # dreapta
                            if index_x < 7 and initiate_matrix[index_y][index_x + 1] >= 0:

                                k = (index_y, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # stanga
                            if index_x > 0 and initiate_matrix[index_y][index_x - 1] >= 0:

                                k = (index_y, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sus
                            if index_y > 0 and initiate_matrix[index_y - 1][index_x] >= 0:

                                k = (index_y - 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y -= 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # jos
                            if index_y < 7 and initiate_matrix[index_y + 1][index_x] >= 0:

                                k = (index_y + 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                    if id_piece in [40, 41]:  # bishooop
                        tempx = index_x
                        tempy = index_y
                        index_y = tempy
                        index_x = tempx
                        while True:  # dreapta jos
                            if index_y < 7 and index_x < 7 and initiate_matrix[index_y + 1][index_x + 1] <= 0:

                                k = (index_y + 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        check_bool = True
                        index_y = tempy
                        index_x = tempx
                        while True:  # stanga sus
                            if index_y > 0 and index_x > 0 and initiate_matrix[index_y - 1][index_x - 1] <= 0:

                                k = (index_y - 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # Dreapta sus
                            if index_y >= 0 and index_x < 7 and initiate_matrix[index_y - 1][index_x + 1] <= 0:

                                k = (index_y - 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sganga jos
                            if index_y < 7 and index_x >= 0 and initiate_matrix[index_y + 1][index_x - 1] <= 0:

                                k = (index_y + 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                            index_y = tempy
                            index_x = tempx

                    if id_piece in [-40, -41]:  # bishooop
                        tempx = index_x
                        tempy = index_y
                        index_y = tempy
                        index_x = tempx
                        while True:  # dreapta jos
                            if index_y < 7 and index_x < 7 and initiate_matrix[index_y + 1][index_x + 1] >= 0:

                                k = (index_y + 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        check_bool = True
                        index_y = tempy
                        index_x = tempx
                        while True:  # stanga sus
                            if index_y > 0 and index_x > 0 and initiate_matrix[index_y - 1][index_x - 1] >= 0:
                                k = (index_y - 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # Dreapta sus

                            if index_y > 0 and index_x < 7 and initiate_matrix[index_y - 1][index_x + 1] >= 0:
                                k = (index_y - 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sganga jos
                            if index_y < 7 and index_x >= 0 and initiate_matrix[index_y + 1][index_x - 1] >= 0:

                                k = (index_y + 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        self.enemy_possible_moves(self.king_position(), initiate_matrix)
                        if len(self.cach_enemy_moves) > 0:
                            return True
                        else:
                            return False

                    if id_piece in [-9]:  # queen
                        tempx = index_x
                        tempy = index_y
                        index_y = tempy
                        index_x = tempx
                        while True:  # dreapta jos
                            if index_y < 7 and index_x < 7 and initiate_matrix[index_y + 1][index_x + 1] >= 0:

                                k = (index_y + 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # stanga sus
                            if index_y > 0 and index_x > 0 and initiate_matrix[index_y - 1][index_x - 1] >= 0:

                                k = (index_y - 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)
                                index_x -= 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # Dreapta sus
                            if index_y >= 0 and index_x < 7 and initiate_matrix[index_y - 1][index_x + 1] >= 0:
                                k = (index_y - 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sganga jos
                            if index_y < 7 and index_x >= 0 and initiate_matrix[index_y + 1][index_x - 1] >= 0:

                                k = (index_y + 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        while True:  # dreapta
                            if index_x < 7 and initiate_matrix[index_y][index_x + 1] >= 0:

                                k = (index_y, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        self.reset_coord(tempy, tempx)
                        while True:  # stanga
                            if index_x > 0 and initiate_matrix[index_y][index_x - 1] >= 0:

                                k = (index_y, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sus
                            if index_y > 0 and initiate_matrix[index_y - 1][index_x] >= 0:

                                k = (index_y - 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y -= 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # jos
                            if index_y < 7 and initiate_matrix[index_y + 1][index_x] >= 0:

                                k = (index_y + 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y += 1
                                if initiate_matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                    if id_piece in [9]:
                        tempx = index_x
                        tempy = index_y
                        index_y = tempy
                        index_x = tempx
                        while True:  # dreapta
                            if index_x < 7 and initiate_matrix[index_y][index_x + 1] <= 0:

                                k = (index_y, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # stanga
                            if index_x > 0 and initiate_matrix[index_y][index_x - 1] <= 0:

                                k = (index_y, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sus
                            if index_y > 0 and initiate_matrix[index_y - 1][index_x] <= 0:

                                k = (index_y - 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # jos
                            if index_y < 7 and initiate_matrix[index_y + 1][index_x] <= 0:

                                k = (index_y + 1, index_x)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_y += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        while True:  # dreapta jos
                            if index_y < 7 and index_x < 7 and initiate_matrix[index_y + 1][index_x + 1] <= 0:

                                k = (index_y + 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # stanga sus
                            if index_y > 0 and index_x > 0 and initiate_matrix[index_y - 1][index_x - 1] <= 0:

                                k = (index_y - 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # Dreapta sus
                            if index_y >= 0 and index_x < 7 and initiate_matrix[index_y - 1][index_x + 1] <= 0:

                                k = (index_y - 1, index_x + 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x += 1
                                index_y -= 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        while True:  # sganga jos
                            if index_y < 7 and index_x >= 0 and initiate_matrix[index_y + 1][index_x - 1] <= 0:

                                k = (index_y + 1, index_x - 1)
                                if k not in self.possible_moves:
                                    self.possible_moves.append(k)

                                index_x -= 1
                                index_y += 1
                                if initiate_matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                    if self.id in [-30, -31]:
                        if index_x + 1 <= 7 and index_y + 2 <= 7 and initiate_matrix[index_y + 2][index_x + 1] >= 0:
                            k = (index_y + 2, index_x + 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 1 >= 0 and index_y + 2 <= 7 and initiate_matrix[index_y + 2][
                            index_x + -1] >= 0:
                            k = (index_y + 2, index_x - 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 2 >= 0 and index_y + 1 <= 7 and initiate_matrix[index_y + 1][index_x - 2] >= 0:
                            k = (index_y + 1, index_x - 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x + 2 <= 7 and index_y + 1 <= 7 and initiate_matrix[index_y + 1][index_x + 2] >= 0:
                            k = (index_y + 1, index_x + 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x + 2 <= 7 and index_y - 1 >= 0 and initiate_matrix[index_y - 1][index_x + 2] >= 0:
                            k = (index_y - 1, index_x + 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 2 >= 0 and index_y - 1 >= 0 and initiate_matrix[index_y - 1][index_x - 2] >= 0:
                            k = (index_y - 1, index_x - 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x + 1 <= 7 and index_y - 2 >= 0 and initiate_matrix[index_y - 2][index_x + 1] >= 0:
                            k = (index_y - 2, index_x + 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 1 >= 0 and index_y - 2 >= 0 and initiate_matrix[index_y - 2][index_x - 1] >= 0:
                            k = (index_y - 2, index_x - 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                    # white knight
                    if id_piece in [30, 31]:
                        if index_x + 1 <= 7 and index_y + 2 <= 7 and initiate_matrix[index_y + 2][index_x + 1] <= 0:
                            k = (index_y + 2, index_x + 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 1 >= 0 and index_y + 2 <= 7 and initiate_matrix[index_y + 2][
                            index_x + -1] <= 0:
                            k = (index_y + 2, index_x - 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 2 >= 0 and index_y + 1 <= 7 and initiate_matrix[index_y + 1][index_x - 2] <= 0:
                            k = (index_y + 1, index_x - 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x + 2 <= 7 and index_y + 1 <= 7 and initiate_matrix[index_y + 1][index_x + 2] <= 0:
                            k = (index_y + 1, index_x + 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x + 2 <= 7 and index_y - 1 >= 0 and initiate_matrix[index_y - 1][index_x + 2] <= 0:
                            k = (index_y - 1, index_x + 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 2 >= 0 and index_y - 1 >= 0 and initiate_matrix[index_y - 1][index_x - 2] <= 0:
                            k = (index_y - 1, index_x - 2)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x + 1 <= 7 and index_y - 2 >= 0 and initiate_matrix[index_y - 2][index_x + 1] <= 0:
                            k = (index_y - 2, index_x + 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

                        if index_x - 1 >= 0 and index_y - 2 >= 0 and initiate_matrix[index_y - 2][index_x - 1] <= 0:
                            k = (index_y - 2, index_x - 1)
                            if k not in self.possible_moves:
                                self.possible_moves.append(k)

    def enemy_possible_moves(self, king_pos, matrix):
        if self.id > 0:
            self.cach_enemy_moves.clear()
            self.enemy_moves.clear()
            for y in matrix:
                index_y = matrix.index(y)
                for x in y:
                    index_x = y.index(x)
                    id = matrix[index_y][index_x]
                    tempy = index_y
                    tempx = index_x
                    if id in [-51, -50]:
                        while True:
                            if index_x < 7 and matrix[index_y][index_x + 1] >= 0:

                                k = (index_y, index_x + 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1
                            print(id)
                            print(matrix[index_y][index_x])
                            if matrix[index_y][index_x] == id:
                                print(id)
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:
                            if index_y > 0 and matrix[index_y - 1][index_x] >= 0:

                                k = (index_y - 1, index_x)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_y -= 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # jos
                            if index_y < 7 and matrix[index_y + 1][index_x] >= 0:

                                k = (index_y + 1, index_x)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_y += 1
                                if matrix[index_y][index_x] > 0:
                                    index_y = tempy
                                    index_x = tempx
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()
                        while True:  # stanga
                            if index_x > 0 and matrix[index_y][index_x - 1] >= 0:

                                k = (index_y, index_x - 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x -= 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            print('yes')
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        print('enemy_moves: %s ' % self.enemy_moves)
                        print('cach: %s' % self.cach_enemy_moves)
                        print(f'number of check: {self.sah_count}')

                    if id in [-40, -41]:
                        index_y = tempy
                        index_x = tempx
                        while True:  # dreapta jos
                            if index_y < 7 and index_x < 7 and matrix[index_y + 1][index_x + 1] >= 0:
                                k = (index_y + 1, index_x + 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x += 1
                                index_y += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break

                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()
                        while True:  # stanga sus
                            if index_y > 0 and index_x > 0 and matrix[index_y - 1][index_x - 1] >= 0:

                                k = (index_y - 1, index_x - 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x -= 1
                                index_y -= 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        while True:  # Dreapta sus
                            if index_y > 0 and index_x < 7 and matrix[index_y - 1][index_x + 1] >= 0:

                                k = (index_y - 1, index_x + 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x += 1
                                index_y -= 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        while True:  # sganga jos
                            if index_y < 7 and index_x > 0 and matrix[index_y + 1][index_x - 1] >= 0:

                                k = (index_y + 1, index_x - 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x -= 1
                                index_y += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)

                        print('enemy_moves: %s ' % self.enemy_moves)
                        print('cach: %s' % self.cach_enemy_moves)
                        print(f'number of check: {self.sah_count}')

                    if id in [-9]:
                        index_y = tempy
                        index_x = tempx

                        while True:  # dreapta jos
                            if index_y < 7 and index_x < 7 and matrix[index_y + 1][
                                index_x + 1] >= 0:

                                k = (index_y + 1, index_x + 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x += 1
                                index_y += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()
                        while True:  # stanga sus
                            if index_y > 0 and index_x > 0 and matrix[index_y - 1][
                                index_x - 1] >= 0:

                                k = (index_y - 1, index_x - 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x -= 1
                                index_y -= 1
                                if matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # Dreapta sus
                            if index_y >= 0 and index_x < 7 and matrix[index_y - 1][
                                index_x + 1] >= 0:

                                k = (index_y - 1, index_x + 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x += 1
                                index_y -= 1
                                if matrix[index_y][index_x] < 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # sganga jos
                            if index_y < 7 and index_x >= 0 and matrix[index_y + 1][
                                index_x - 1] >= 0:

                                k = (index_y + 1, index_x - 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x -= 1
                                index_y += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # dreapta
                            if index_x < 7 and matrix[index_y][index_x + 1] >= 0:

                                k = (index_y, index_x + 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # stanga
                            if index_x > 0 and matrix[index_y][index_x - 1] >= 0:

                                k = (index_y, index_x - 1)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_x -= 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # sus
                            if index_y > 0 and matrix[index_y - 1][index_x] >= 0:

                                k = (index_y - 1, index_x)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_y -= 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        while True:  # jos
                            if index_y < 7 and matrix[index_y + 1][index_x] >= 0:

                                k = (index_y + 1, index_x)
                                if k not in self.enemy_moves:
                                    self.enemy_moves.append(k)

                                index_y += 1
                                if matrix[index_y][index_x] > 0:
                                    break
                            else:
                                break
                        index_y = tempy
                        index_x = tempx

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()
                        print('enemy_moves: %s ' % self.enemy_moves)
                        print('cach: %s' % self.cach_enemy_moves)
                        print(f'number of check: {self.sah_count}')

                    if id in [-30, -31]:
                        if index_x + 1 <= 7 and index_y + 2 <= 7 and matrix[index_y + 2][index_x + 1] >= 0:

                            k = (index_y + 2, index_x + 1)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x - 1 >= 0 and index_y + 2 <= 7 and matrix[index_y + 2][
                            index_x + -1] >= 0:
                            k = (index_y + 2, index_x - 1)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x - 2 >= 0 and index_y + 1 <= 7 and matrix[index_y + 1][index_x - 2] >= 0:

                            k = (index_y + 1, index_x - 2)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x + 2 <= 7 and index_y + 1 <= 7 and matrix[index_y + 1][index_x + 2] >= 0:
                            k = (index_y + 1, index_x + 2)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x + 2 <= 7 and index_y - 1 >= 0 and matrix[index_y - 1][index_x + 2] >= 0:
                            k = (index_y - 1, index_x + 2)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x - 2 >= 0 and index_y - 1 >= 0 and matrix[index_y - 1][index_x - 2] >= 0:
                            k = (index_y - 1, index_x - 2)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x + 1 <= 7 and index_y - 2 >= 0 and matrix[index_y - 2][index_x + 1] >= 0:
                            k = (index_y - 2, index_x + 1)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_x - 1 >= 0 and index_y - 2 >= 0 and matrix[index_y - 2][index_x - 1] >= 0:
                            k = (index_y - 2, index_x - 1)
                            if k not in self.enemy_moves:
                                self.enemy_moves.append(k)

                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()
                        print('enemy_moves: %s ' % self.enemy_moves)
                        print('cach: %s' % self.cach_enemy_moves)
                        print(f'number of check: {self.sah_count}')

                    if id in [-11, -12, -13, -14, -15, -16, -17, -18]:

                        tempx = index_x
                        tempy = index_y
                        if initiate_matrix[index_y + 1][index_x] == 0:
                            if index_y == 1:
                                p = 0
                                while p <= 1:
                                    if initiate_matrix[index_y + 1][index_x] == 0:
                                        k = (index_y + 1, index_x)
                                        self.enemy_moves.append(k)
                                        index_y += 1
                                    p += 1

                                index_y = tempy
                                index_x = tempx

                            else:
                                if initiate_matrix[index_y + 1][index_x] == 0:
                                    if 0 == initiate_matrix[index_y + 1][index_x]:
                                        k = (index_y + 1, index_x)
                                        self.enemy_moves.append(k)
                                        index_y = tempy
                                        index_x = tempx
                        if index_x - 1 > 0 and index_y < 7:
                            if initiate_matrix[index_y + 1][index_x - 1] > 0 :
                                k = (index_y + 1, index_x - 1)
                                self.enemy_moves.append(k)
                            index_y = tempy
                            index_x = tempx
                        if king_pos in self.enemy_moves:
                            self.sah_count += 1

                            print('yes')
                            if matrix[index_y][index_x] == id:
                                self.cach_enemy_moves.append((index_y, index_x))
                            for i in self.enemy_moves:
                                self.cach_enemy_moves.append(i)
                        self.enemy_moves.clear()

                        if index_y < 6 and index_x < 6:
                            if initiate_matrix[index_y + 1][index_x + 1] > 0:
                                k = (index_y + 1, index_x + 1)
                                self.enemy_moves.append(k)
                            index_y = tempy
                            index_x = tempx

                            if king_pos in self.enemy_moves:
                                self.sah_count += 1

                                print('yes')
                                if matrix[index_y][index_x] == id:
                                    self.cach_enemy_moves.append((index_y, index_x))
                                for i in self.enemy_moves:
                                    self.cach_enemy_moves.append(i)
                            self.enemy_moves.clear()
                            index_y = tempy
                            index_x = tempx




    def king_position(self):
        for i in initiate_matrix:
            index_y = initiate_matrix.index(i)
            for j in i:
                index_x = i.index(j)
                if self.id > 0 and j == 10:
                    king_pos = (index_y, index_x)
                    return king_pos

    def reset_coord(self, tempy, tempx):
        self.y_pos = tempy
        self.x_pos = tempx

    def move_pieces(self, m, n, ):
        initiate_matrix[self.y_pos][self.x_pos] = 0
        initiate_matrix[m][n] = self.id
        for i in initiate_matrix:
            print(i)

        self.sah_count = 0

        print("\n")

# pg.draw.rect(screen, (73, 73, 105), (index_j * 100, index_k * 100, 100, 100))
