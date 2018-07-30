#coding: utf-8

import numpy as np

from pattern import Pattern
from setting import ELEMENT, COLOR, SCORE, DIRECT


class Board():
    def __init__(self, row=5, col=5):
        '''生成初始矩阵，可能存在满足三消的情况，在别的函数再处理
        假定五种颜色，用1~5来表示，0用来标记待消除的瞬态
        同时创建备份矩阵，当尝试寻找可消除块时，将原始状态备份，尝试完后需要复原
        '''
        #参数检查
        assert(row>0 and col>0)
        #保存输入维度参数
        self.__row = row
        self.__col = col
        #创建初始矩阵
        self.__bd = np.random.randint(low=1, high=6, size=(row, col))  #从1到5，代表5种颜色
        #创建备份矩阵
        self.__bd_backup = np.zeros((row, col), np.int)
        self.__flag_backup = False

    def reinit(self, clean_backup=True):
        '''重新初始化矩阵，清除备份矩阵
        '''
        row = self.__row
        col = self.__col
        self.__bd = np.random.randint(low=1, high=6, size=(row, col))  #从1到5，代表5种颜色
        if clean_backup:  #同时清空备份
            self.__bd_backup = np.zeros((row, col), np.int)
            self.__flag_backup = False

    def save(self):
        '''备份矩阵，设置flag
        '''
        self.__bd_backup = self.__bd
        self.__flag_backup = True

    def load(self):
        '''还原矩阵，仅在备份过之后才能还原，且还原时清除备份flag
        '''
        if self.__flag_backup == True:
            self.__bd = self.__bd_backup
            self.__flag_backup = False
        else:
            print("LOAD FAILED")
            pass
       
    def match(self, patterns, color):
        '''查找并标记满足条件的块
        '''
        row = self.__row
        col = self.__col
        #纵横四方向外各扩张两行，填充0
        bd_ext = np.zeros((row+4, col+4), np.int) 
        bd_ext[2:-2, 2:-2] = self.__bd
        #print(bd_ext) 
        area_count = 0
        for pt in patterns:
            for i in range(row):
                for j in range(col):
                    area_scan = bd_ext[i:i+5, j:j+5] #能遍历整个矩阵，每次取出5*5的方阵，与传入的pattern作比较
                    if (area_scan*pt == color*pt).all(): #5*5的方阵中，与传入的pattern位置相同的格子正好都是满足要求的颜色
                        area_count += 1
                        bd_ext[i:i+5, j:j+5] = area_scan*(1-pt) #将传入的pattern取反和5*5方阵相乘，保留其它格子不变，pattern部分变成0
            yield area_count
        self.__bd = bd_ext[2:-2, 2:-2]


    def boom(self):
        '''遍历所有的pattern，将5格，4格，3格的情况找出来，返回每种格数每种颜色消除的次数
        '''
        pt = Pattern()
        pts_5 = pt.get_by_name("5")
        pts_4 = pt.get_by_name("4")
        pts_3 = pt.get_by_name("3")
        pts_list = [pts_5, pts_4, pts_3]
        
        #结果存放每种pattern下，每种颜色消除的次数，作为返回值
        cnt_boom = np.zeros((3, 5), np.int)  
        
        #分格数（5,4,3格），颜色，统计当前消去各多少
        for i, pts in enumerate(pts_list):
            for j, color in enumerate(COLOR):
                for cnt in self.match(pts, color):
                    pass
                cnt_boom[i][j] = cnt
        #print(cnt_boom)
        return cnt_boom

    def score(self, cnt_boom, clr=0):
        '''基于boom的结果，给出一个按照颜色分类的分数
        '''
        sc_level_5 = SCORE["5"]
        sc_level_4 = SCORE["4"]
        sc_level_3 = SCORE["3"]
        
        #每种颜色得到的分数
        sc = [cnt_boom[0][i]*sc_level_5 + cnt_boom[1][i]*sc_level_4 + cnt_boom[2][i]*sc_level_3 for i in range(5)]
        for j, color in enumerate(COLOR):
            if color == clr:
                return sc[j]
        return sum(sc)

    def down(self, direction=0):
        '''往一个方向按照‘重力’填补空缺，0左，1上，2右，3下
        '''
        row = self.__row
        col = self.__col

        # 先统一把方向转成向左，因为左方向最方便计算
        if direction == DIRECT["LEFT"]:
            pass
        elif direction == DIRECT["UP"]:
            self.__bd = np.transpose(self.__bd)
            row, col = col, row
        elif direction == DIRECT["RIGHT"]:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
        elif direction == DIRECT["DOWN"]:
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
            row, col = col, row
            
        # 对于所有行，每一列中，从左到右凡是遇到空格，把该格右边的所有格，复制到当前格开始到倒数第二格且最后一格填0. 某格右边全0时这一行完成
        for i in range(row):
            for j in range(col-1):
                while self.__bd[i][j] == 0:
                    self.__bd[i][j:-1] = self.__bd[i][j+1:]
                    self.__bd[i][-1] = 0
                    if sum(self.__bd[i][j:]) == 0:
                        break
        
        # 再转回去              
        if direction == DIRECT["LEFT"]:
            pass      
        if direction == DIRECT["UP"]:
            self.__bd = np.transpose(self.__bd)
        if direction == DIRECT["RIGHT"]:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
        if direction == DIRECT["DOWN"]:
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
                    self.__bd[i][j] = np.random.randint(low=1, high=6) #1~5五种颜色

    def swap(self, cell_a, cell_b):
        '''交换相邻两格
        '''
        row = self.__row
        col = self.__col
        #判断输入数据[a0,a1] [b0,b1]是否valid，是否相邻
        if cell_a[0] in range(row) and cell_a[1] in range(col) and cell_b[0] in range(row) and cell_b[1] in range(col) and \
            ((abs(cell_a[0]-cell_b[0]) == 1 and cell_a[1] == cell_b[1]) or (cell_a[0] == cell_b[0] and abs(cell_a[1] - cell_b[1]) == 1)):
            #相邻的话，交换两格
            self.__bd[cell_a[0]][cell_a[1]], self.__bd[cell_b[0]][cell_b[1]] = self.__bd[cell_b[0]][cell_b[1]], self.__bd[cell_a[0]][cell_a[1]]
            return True
        else:
            return False
    '''
    TODO
    '''


    def temp(self, cell_a, cell_b):
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

    def paint(self):
        '''绘制矩阵，初始用打印语句代替
        TODO: 相邻同色块要不要做标记？
        '''
        print(self.__bd)

    
if __name__ == '__main__':
    print("="*10, "Test Board")
    pt = Pattern()
    bd = Board(5, 6) #最好用不同的数作为两个维度，更好的测试出问题（例如两个维度颠倒）
    
    #Test init/paint
    if True:
        print("-"*10, "Test init")
        bd.paint()
        
    #Test reinit
    if True:
        print("-"*10, "Test reinit")
        bd.reinit()
        bd.paint()
        
    #Test save/load
    if True:
        print("-"*10, "Test save/load")
        bd.paint()
        bd.save()
        bd.reinit(clean_backup = False) #测试时去掉清空备份的选项
        bd.paint()
        bd.load()
        bd.paint()
        
    #Test match patterns
    if True:
        print("-"*10, "Test match")
        bd.save()
        bd.paint()
        for color in COLOR:
            print("    Color: %s" % COLOR[color])
            for cnt in bd.match(pt.get_by_name("3"), color):
                print("    Matched: %d" % cnt)  #每种pattern找到了几个（看增量，叠加在之前的上）
        bd.paint()  #退出迭代器后，应该将标记0的变化体现到原始矩阵上
        bd.load()
        #bd.paint()  #应该还原了

    #Test boom
    if True:
        print("-"*10, "Test boom")
        bd.save()
        bd.paint()
        res = bd.boom() #计算出每种格数，每种颜色，分别消除了多少次；同时把消除的格子标记0
        bd.paint()  #消除后的矩阵
        print(res)  #消除的次数（3*5矩阵表示结果）
        bd.load()
        #bd.paint()

    #Test score
    if True:
        print("-"*10, "Test score")
        bd.save()
        bd.paint()
        cnt_boom = bd.boom() #计算出每种格数，每种颜色，分别消除了多少次；同时把消除的格子标记0
        bd.paint()  #消除后的矩阵
        for color in COLOR:
            print("    %s: %d" % (COLOR[color], bd.score(cnt_boom, color)))
        print("    ALL: %d" % bd.score(cnt_boom))
        bd.load()
        #bd.paint()
        
    #Test down
    if True:
        print("-"*10, "Test down")
        bd.save()
        bd.paint()
        while bd.score(bd.boom()) == 0:
            bd.reinit(clean_backup = False) #如果碰到没有可消除的情形，临时生成新数据，并且不破坏原始备份
            bd.paint()
        bd.paint()
        for direct in DIRECT: 
            print(direct)
            bd.down(DIRECT[direct])
            bd.paint()
        bd.load()
        #bd.paint()

    #Test fill
    if True:
        print("-"*10, "Test fill")
        bd.save()
        bd.paint()
        while bd.score(bd.boom()) == 0:
            bd.reinit(clean_backup = False) #如果碰到没有可消除的情形，临时生成新数据，并且不破坏原始备份
            bd.paint()
        bd.paint()
        bd.down()
        bd.paint()
        bd.fill()
        bd.paint()
        bd.load()
        #bd.paint()

    #Test swap
    if True:
        print("-"*10, "Test swap")
        bd.save()
        bd.paint()
        for cell_a, cell_b in [((1,1),(1,2)), ((3,2),(2,2)),((3,1),(2,2))]:
            print(bd.swap(cell_a, cell_b), cell_a, cell_b)
            bd.paint()
        bd.load()
        #bd.paint()


'''        
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
'''
