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


if __name__ == '__main__':
    args = get_args()
    bd = Board(args.row, args.col)

    round = 1
    score = [0, 0, 0, 0, 0]
    while True:
        while True:
            cnt_boom = bd.boom()
            if bd.score(cnt_boom) == 0:
                break
            else:
                for i, color in enumerate(COLOR):
                    score[i] += bd.score(cnt_boom, color)
            #bd.paint() 
            bd.down(DIRECT["DOWN"])
            #bd.paint()
            bd.fill()
            #bd.paint()
        print("\n== DOWN ==")
        bd.paint()
        print("\n~~ SCORE~~")
        print(score)
        #print("? 2 ? ", time.asctime())
        print("\n--------------------\nROUND %d" % round)
        pair = bd.hint(args.hint)
        if pair is None:
            print("DEAD")
            bd.reinit()
            bd.paint()
        #input("")
        time.sleep(1)
        bd.swap(pair[0], pair[1])   
        print("\n-- MOVE --")
        bd.paint()
        round += 1
