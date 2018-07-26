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

    def map(self, mark=1):
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

    def boom(self):
        return self.map(mark=1)

    def scan(self):
        return self.map(mark=0)
    
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

    def swap(self, cell_a, cell_b):
        '''交换相邻两格，并且判断是否能触发至少一个消除
        '''
        row = self.__row
        col = self.__col

        try:
            assert(cell_a[0] in range(row) and cell_a[1] in range(col)) #判断输入数据[a0,a1] [b0,b1]是否valid，是否相邻
            assert(cell_b[0] in range(row) and cell_b[1] in range(col))
            assert(abs(cell_a[0]-cell_b[0]) == 1 and cell_a[1] == cell_b[1]) or (cell_a[0] == cell_b[0] and abs(cell_a[1] - cell_b[1]) == 1)
        except AssertionError:
            print("invalid parameter")
            return False
            
        ''' 确定当前没有未消除的部分，不放在这里执行，否则多次判断影响效率
        try:
            _, score = self.score(self.scan())
            assert(score == 0)
        except AssertionError:
            print("not clean base")
            return False
        '''

        '''尝试交换相邻两块，然后看是否能产生新的消除块，如果不能，要还原这两块
        其实不需要扫描整个矩阵，只需要相邻的部分，考虑到其实也差不多6*6的区域，而总的区域也不会太大，就整体扫描了
        '''
        self.__bd[cell_a[0]][cell_a[1]], self.__bd[cell_b[0]][cell_b[1]] = self.__bd[cell_b[0]][cell_b[1]], self.__bd[cell_a[0]][cell_a[1]]
        try:
            _, score = self.score(self.scan())
            assert(score > 0)
        except AssertionError:
            self.__bd[cell_a[0]][cell_a[1]], self.__bd[cell_b[0]][cell_b[1]] = self.__bd[cell_b[0]][cell_b[1]], self.__bd[cell_a[0]][cell_a[1]]
            #print("invalid move, revert")
            return False

        return True
        
    def propose(self):
        '''遍历整个矩阵，计算交换相邻格带来的收益，从而给出建议，如果收益相同则随机给一个
        如果没有任何可以交换的格子，说明这一局‘死了’，可能需要重新开局或者打乱
        '''
        row = self.__row
        col = self.__col

        count = 0
        res = []
        for i in range(row-1):
            for j in range(col-1):
                if self.swap([i,j], [i,j+1]):
                    _, score = self.score(self.scan()) #算出交换后的分数
                    self.__bd[i][j], self.__bd[i][j+1] = self.__bd[i][j+1], self.__bd[i][j] #先还原
                    res.append([score, [i,j], [i,j+1]])
                    count += 1
                if self.swap([i,j], [i+1,j]):
                    _, score = self.score(self.scan()) #算出交换后的分数
                    self.__bd[i][j], self.__bd[i+1][j] = self.__bd[i+1][j], self.__bd[i][j] #先还原
                    res.append([score, [i,j], [i+1,j]])
                    count += 1
        #print(count, res)
        np.random.shuffle(res)
        res.sort(key=lambda x:x[0], reverse=True)
        #print(count, res)
        return count, res

    def reinit(self):
        cnt, _ = self.propose()
        if cnt == 0:
            pass
        else:
            pass #只要有能交换的相邻格，就不用重新开局或者打乱

    def paint(self):
        '''绘制矩阵，初始用打印语句代替
        TODO: 相邻同色块要不要做标记？
        '''
        print()
        print(self.__bd)

    
if __name__ == '__main__':
    pt = Pattern()
    bd = Board(5, 5)
    bd.paint()
    res = bd.boom()
    #print(bd.score(res))
    bd.paint()
    bd.down(3)
    bd.paint()
    bd.fill()
    bd.paint()
    print(bd.swap((1,1),(2,1)))
    bd.paint()
    bd.propose()
    bd.paint()
