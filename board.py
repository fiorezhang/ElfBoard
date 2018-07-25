#coding: utf-8

import numpy as np

from pattern import Pattern
from color import COLOR


class Board():
    def __init__(self, row, col):
        '''生成初始矩阵，可能存在满足三消的情况，在别的函数再处理
        假定五种颜色，用1~5来表示，0用来标记待消除的瞬态
        '''
        assert(row>0 and col>0)
        self.__row = row
        self.__col = col
        self.__bd = np.random.randint(low=1, high=6, size=(row, col))  #从1到5，代表5种颜色
       
    def match(self, patterns, color, mark=0):
        '''标记满足条件的块，按照优先级来扫描，如五连》五折》四条》四块》三条
        '''
        row = self.__row
        col = self.__col

        bd_ext = np.zeros((row+4, col+4), np.int) #纵横四方向外各扩张两行，填充0
        bd_ext[2:-2, 2:-2] = self.__bd
        #print(bd_ext)
        
        marks = []
        count = 0
        for pattern in patterns:
            for i in range(row):
                for j in range(col):
                    cells = bd_ext[i:i+5, j:j+5]
                    if (cells*pattern == color*pattern).all():
                        count += 1
                        marks.append([i,j])
                        if mark == 1:
                            bd_ext[i:i+5, j:j+5] = cells*(1-pattern)
        if mark == 1:
            self.__bd = bd_ext[2:-2, 2:-2]
            #print(self.__bd)
        return count, marks 

    def boom(self):
        pt = Pattern()
        pts_all = [pt.get_5_l(), pt.get_5_b(), pt.get_4_l(), pt.get_4_s(), pt.get_3_l()]
        bm_cnt_all = []
        for pts in pts_all:
            bm_cnt_color = []
            for color in COLOR: 
                bm_cnt, _ = self.match(pts, color, mark=1)
                print(bm_cnt)
                bm_cnt_color.append(bm_cnt)
            print(bm_cnt_color)
            bm_cnt_all.append(bm_cnt_color)
        print(bm_cnt_all)
        return bm_cnt_all
    
    def score(self, bm_cnt):
        sc = [bm_cnt[0][i]*4 + bm_cnt[1][i]*4 + bm_cnt[2][i]*2 + bm_cnt[3][i]*2 + bm_cnt[4][i] for i in range(5)]
        return sc

    def fill(self, direction=0):
        '''往一个方向按照‘重力’填补空缺，0左，1上，2右，3下
        '''
        pass

    def paint(self):
        '''绘制矩阵，初始用打印语句代替
        TODO: 相邻同色块要不要做标记？
        '''
        print(self.__bd)

    
if __name__ == '__main__':
    pt = Pattern()
    bd = Board(9, 9)
    bd.paint()
    res = bd.boom()
    print(bd.score(res))
    print(sum(bd.score(res)))
    bd.paint()
