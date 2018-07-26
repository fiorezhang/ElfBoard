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

    round = 0
    while True:
        print("ROUND %d" % round)
        bd.paint()
        while bd.score(bd.boom())[1] > 0:
            bd.paint() 
            bd.down(3)
            bd.paint()
            bd.fill()
            bd.paint()
        cnt, cells = bd.propose()
        if cnt == 0:
            print("DEAD")
            #bd.reinit()
            break
        _, cell_a, cell_b = cells[0] #这里的分数不准确，因为重复计算了
        #input("")
        time.sleep(1)
        bd.swap((cell_a[0], cell_a[1]), (cell_b[0], cell_b[1]))   
        round += 1
