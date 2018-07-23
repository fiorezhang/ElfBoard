#coding: utf-8

import numpy as np

class Board():
    def __init__(self, row, col):
        '''生成初始矩阵，可能存在满足三消的情况，在别的函数再处理
        假定五种颜色，用1~5来表示，0用来标记待消除的瞬态
        '''
        assert(row>0 and col>0)
        self.bd = np.random.randint(low=1, high=6, size=(row, col))
       
    def match(self, pattern):
        '''标记满足条件的块，按照优先级来扫描，如五连》五折》四条》四块》三条
        '''
        pass
    
    def paint(self):
        '''绘制矩阵，初始用打印语句代替
        TODO: 相邻同色块要不要做标记？
        '''
        print(self.bd)

    
if __name__ == '__main__':
    bd = Board(8, 6)
    bd.paint()