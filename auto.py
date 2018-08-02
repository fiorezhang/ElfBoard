#coding: utf-8

import numpy as np
import argparse
import time

from board import Board
from setting import ELEMENT, COLOR, SCORE, DIRECT

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--row", type=int, default=0)
    parser.add_argument("--col", type=int, default=0)
    parser.add_argument("--hint", type=int, default=1)
    args = parser.parse_args()
    return args

def clean_board(bd):
    '''清理直到没有可以自动消除的块，但是有通过交换相邻块可以消除的块
    '''
    while True:
        #此处的boom不计算分数，刚开局以及碰到死局重开时，需要做必要的清理
        while bd.score(bd.boom()) > 0: #自动消除，填充，直到没有可自动消除的块
            bd.down()
            bd.fill()
        #寻找是否有可以消除的块
        pair = bd.hint(args.hint)
        if not pair is None:
            break
        print("\n** DEAD **")
        bd.reinit()
    bd.paint()
    return pair


if __name__ == '__main__':
    args = get_args()
    bd = Board(args.row, args.col)
    clean_board(bd)

    round = 0
    score = [0, 0, 0, 0, 0]
    score_c = [0, 0, 0, 0, 0]
    bonus_5 = [0, 0, 0, 0, 0]
    bonus_5_c = [0, 0, 0, 0, 0]
    bonus_4 = [0, 0, 0, 0, 0]
    bonus_4_c = [0, 0, 0, 0, 0]
    bonus_3 = [0, 0, 0, 0, 0]
    bonus_3_c = [0, 0, 0, 0, 0]
    while True:
        print("\n--------------------\nROUND %d" % round)
        round += 1
        pair = clean_board(bd)
        time.sleep(1)
        bd.swap(pair[0], pair[1])   
        print("\n-- MOVE --")
        bd.paint()
        
        while True:
            cnt_boom = bd.boom()
            if bd.score(cnt_boom) == 0:
                break
            else:
                for i, color in enumerate(COLOR):
                    score_c[i] = bd.score(cnt_boom, color)
                    score[i] += score_c[i]
                    bonus_5_c[i] = cnt_boom[0][i]
                    bonus_5[i] += bonus_5_c[i]
                    bonus_4_c[i] = cnt_boom[1][i]
                    bonus_4[i] += bonus_4_c[i]
                    bonus_3_c[i] = cnt_boom[2][i]
                    bonus_3[i] += bonus_3_c[i]
            #bd.paint() 
            bd.down(DIRECT["DOWN"])
            #bd.paint()
            bd.fill()
            #bd.paint()
        print("\n== DOWN ==")
        bd.paint()
        print("\n~~ SCORE~~")
        print(score)
        print(bonus_5)
        print(bonus_4)
        print(bonus_3)
        #print("? 2 ? ", time.asctime())
