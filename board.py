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
       
    def match(self, patterns, color, mark=1):
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

    def boom(self, mark=1):
        '''遍历所有的pattern，将5格，4格，3格的情况找出来，如果mark设置为1，则将找出来的块颜色抹去，避免重复
        '''
        pt = Pattern()
        pts_all = [pt.get_5cs(), pt.get_4cs(), pt.get_3cs()]
        bm_cnt_all = []
        for pts in pts_all:
            bm_cnt_color = []
            for color in COLOR: 
                bm_cnt, _ = self.match(pts, color, mark) #mark设置为1，统计过的标记为0，避免低优先级的重复计算
                #print(bm_cnt)
                bm_cnt_color.append(bm_cnt)
            #print(bm_cnt_color)
            bm_cnt_all.append(bm_cnt_color)
        #print(bm_cnt_all)
        return bm_cnt_all
    
    def score(self, bm_cnt):
        '''基于boom的结果，给出一个按照颜色分类的分数
        '''
        PNT_5 = 4
        PNT_4 = 2
        PNT_3 = 1
        sc = []
        sc_all = 0
        sc = [bm_cnt[0][i]*PNT_5 + bm_cnt[1][i]*PNT_4 + bm_cnt[2][i]*PNT_3 for i in range(5)]
        sc_all = sum(sc)
        return sc, sc_all

    def down(self, direction=0):
        '''往一个方向按照‘重力’填补空缺，0左，1上，2右，3下
        '''
        row = self.__row
        col = self.__col

        if direction == 0:
            pass
        if direction == 1:
            self.__bd = np.transpose(self.__bd)
            row, col = col, row
        if direction == 2:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
        if direction == 3:
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
            row, col = col, row
            
        for i in range(row):
            for j in range(col-1):
                while self.__bd[i][j] == 0:
                    self.__bd[i][j:-1] = self.__bd[i][j+1:]
                    self.__bd[i][-1] = 0
                    if sum(self.__bd[i][j:]) == 0:
                        break
                      
        if direction == 0:
            pass      
        if direction == 1:
            self.__bd = np.transpose(self.__bd)
        if direction == 2:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
        if direction == 3:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]

    def fill(self):
        '''用随机颜色填充0的格子
        '''
        row = self.__row
        col = self.__col
        for i in range(row):
            for j in range(col):
                if self.__bd[i][j] == 0:
                    self.__bd[i][j] = np.random.randint(low=1, high=6)

    def paint(self):
        '''绘制矩阵，初始用打印语句代替
        TODO: 相邻同色块要不要做标记？
        '''
        print()
        print(self.__bd)

    
if __name__ == '__main__':
    pt = Pattern()
    bd = Board(10, 8)
    bd.paint()
    res = bd.boom(1)
    #print(bd.score(res))
    bd.paint()
    bd.down(3)
    bd.paint()
    bd.fill()
    bd.paint()
