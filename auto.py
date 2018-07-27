#coding: utf-8

import numpy as np
import argparse
import time

from board import Board


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--row", type=int, default=0)
    parser.add_argument("--col", type=int, default=0)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    bd = Board(args.row, args.col)

    round = 1
    score = [0, 0, 0, 0, 0]
    while True:
        #print("? 1 ? ", time.asctime())
        while True:
            sc, sc_all = bd.score(bd.boom())
            if sc_all == 0:
                break
            else:
                for i in range(5):
                    score[i] += sc[i]
            #bd.paint() 
            bd.down(3)
            #bd.paint()
            bd.fill()
            #bd.paint()
        print("\n== DOWN ==")
        bd.paint()
        print("\n~~ SCORE~~")
        print(score)
        #print("? 2 ? ", time.asctime())
        print("\n--------------------\nROUND %d" % round)
        cnt, cells = bd.propose()
        if cnt == 0:
            print("DEAD")
            #bd.reinit()
            break
        _, cell_a, cell_b = cells[0] #这里的分数不准确，因为重复计算了
        #input("")
        #time.sleep(1)
        bd.swap((cell_a[0], cell_a[1]), (cell_b[0], cell_b[1]))   
        print("\n-- MOVE --")
        bd.paint()
        round += 1
