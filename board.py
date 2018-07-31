#coding: utf-8

import numpy as np
import datetime

from pattern import Pattern
from setting import ELEMENT, COLOR, SCORE, DIRECT

def performance(f):
    '''修饰器，给函数加时间戳统计运行时间，不用时关掉
    '''
    def fn(*args, **kw):
        t1 = datetime.datetime.now()
        r = f(*args, **kw)
        t2 = datetime.datetime.now()
        print('call %s() in %fs' % (f.__name__, (t2 - t1).total_seconds()))
        return r
    return fn

class Board():
    #@performance
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

    #@performance
    def reinit(self, clean_backup=True):
        '''重新初始化矩阵，清除备份矩阵
        '''
        row = self.__row
        col = self.__col
        self.__bd = np.random.randint(low=1, high=6, size=(row, col))  #从1到5，代表5种颜色
        if clean_backup:  #同时清空备份
            self.__bd_backup = np.zeros((row, col), np.int)
            self.__flag_backup = False

    #@performance
    def save(self):
        '''备份矩阵，设置flag
        '''
        self.__bd_backup = self.__bd.copy()
        self.__flag_backup = True

    #@performance
    def load(self):
        '''还原矩阵，仅在备份过之后才能还原，且还原时清除备份flag
        '''
        if self.__flag_backup == True:
            self.__bd = self.__bd_backup.copy()
            self.__flag_backup = False
        else:
            print("LOAD FAILED")
            pass
       
    #@performance
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
                    if area_scan[2][2] == color and (area_scan*pt == color*pt).all(): #5*5的方阵中，中心格子[2][2]，以及与传入的pattern位置相同的格子正好都是满足要求的颜色
                        area_count += 1
                        bd_ext[i:i+5, j:j+5] = area_scan*(1-pt) #将传入的pattern取反和5*5方阵相乘，保留其它格子不变，pattern部分变成0
            yield area_count
        self.__bd = bd_ext[2:-2, 2:-2]

    #@performance
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

    #@performance
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

    #@performance
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
        elif direction == DIRECT["UP"]:
            self.__bd = np.transpose(self.__bd)
        elif direction == DIRECT["RIGHT"]:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]
            self.__bd = np.transpose(self.__bd)
        elif direction == DIRECT["DOWN"]:
            self.__bd = np.transpose(self.__bd)
            self.__bd = self.__bd[::-1]

    #@performance
    def down_step(self, direction=0):
        '''往一个方向按照‘重力’填补空缺，0左，1上，2右，3下
        生成器，每次移动一行/列
        '''
        row = self.__row
        col = self.__col
        
        if direction == DIRECT["LEFT"]:   
            for j in range(col-1):
                for i in range(row):
                    if self.__bd[i][col-2-j] == 0:
                        self.__bd[i][col-2-j:-1] = self.__bd[i][col-1-j:]
                        self.__bd[i][-1] = 0
                yield
        elif direction == DIRECT["UP"]:   
            for i in range(row-1):
                self.__bd = np.transpose(self.__bd)
                for j in range(col):
                    if self.__bd[j][row-2-i] == 0:
                        self.__bd[j][row-2-i:-1] = self.__bd[j][row-1-i:]
                        self.__bd[j][-1] = 0
                self.__bd = np.transpose(self.__bd)
                yield
        elif direction == DIRECT["RIGHT"]:   
            for j in range(col-1):
                for i in range(row):
                    if self.__bd[i][j+1] == 0:
                        self.__bd[i][1:j+2] = self.__bd[i][:j+1]
                        self.__bd[i][0] = 0
                yield
        elif direction == DIRECT["DOWN"]:   
            for i in range(row-1):
                self.__bd = np.transpose(self.__bd)
                for j in range(col):
                    if self.__bd[j][i+1] == 0:
                        self.__bd[j][1:i+2] = self.__bd[j][:i+1]
                        self.__bd[j][0] = 0
                self.__bd = np.transpose(self.__bd)
                yield                
        
    #@performance
    def fill(self):
        '''用随机颜色填充0的格子
        '''
        row = self.__row
        col = self.__col
        for i in range(row):
            for j in range(col):
                if self.__bd[i][j] == 0:
                    self.__bd[i][j] = np.random.randint(low=1, high=6) #1~5五种颜色
                    
    #@performance
    def fill_step(self, direction=0):
        '''用随机颜色填充0的格子
        生成器，每次填充一行/列
        '''
        row = self.__row
        col = self.__col
        
        if direction == DIRECT["LEFT"]:   
            for j in range(col):
                for i in range(row):
                    if self.__bd[i][j] == 0:
                        self.__bd[i][j] = np.random.randint(low=1, high=6) #1~5五种颜色 
                yield                   
        elif direction == DIRECT["UP"]:   
            for i in range(row):
                for j in range(col):
                    if self.__bd[i][j] == 0:
                        self.__bd[i][j] = np.random.randint(low=1, high=6) #1~5五种颜色 
                yield                   
        elif direction == DIRECT["RIGHT"]:
            for j in range(col):
                for i in range(row):
                    if self.__bd[i][col-1-j] == 0:
                        self.__bd[i][col-1-j] = np.random.randint(low=1, high=6) #1~5五种颜色 
                yield                   
        elif direction == DIRECT["DOWN"]:
            for i in range(row):
                for j in range(col):
                    if self.__bd[row-1-i][j] == 0:
                        self.__bd[row-1-i][j] = np.random.randint(low=1, high=6) #1~5五种颜色 
                yield                   

    #@performance
    def swap(self, a, b):
        '''交换相邻两格
        '''
        row = self.__row
        col = self.__col
        #判断输入数据[a0,a1] [b0,b1]是否valid，是否相邻
        if a[0] in range(row) and a[1] in range(col) and b[0] in range(row) and b[1] in range(col) and \
            ( (abs(a[0]-b[0]) == 1 and a[1] == b[1]) or (a[0] == b[0] and abs(a[1] - b[1]) == 1) ):
            #相邻的话，交换两格
            self.__bd[a[0]][a[1]], self.__bd[b[0]][b[1]] = self.__bd[b[0]][b[1]], self.__bd[a[0]][a[1]]
            return True
        else:
            return False

    #@performance
    def hint(self, best=1):
        '''遍历矩阵，尝试给出符合条件的提示（两个相邻格），同样分数下随机给出提示
        '''
        row = self.__row
        col = self.__col

        #生成随机队列，每个元素是一个相邻格的对子，包括横纵方向
        pair_list_h = [((i,j),(i,j+1)) for i in range(row) for j in range(col-1)]
        pair_list_v = [((i,j),(i+1,j)) for i in range(row-1) for j in range(col)]
        pair_list = pair_list_h + pair_list_v
        np.random.shuffle(pair_list)
        
        #给出一组解，best为0时，给出从随机数列中找到至少能消除一组的第一个解；best为1时，计算所有满足条件的分数
        pair_hint = None
        if best == 0:
            for pair in pair_list:
                self.save()
                self.swap(pair[0], pair[1])
                score = self.score(self.boom())
                if score > 0:
                    pair_hint = pair
                    #print(score, pair)
                self.load()
                if not pair_hint is None:
                    break
        else:
            pair_hint_list = []
            for pair in pair_list:
                self.save()
                self.swap(pair[0], pair[1])
                score = self.score(self.boom())
                if score > 0:
                    pair_hint_list.append([score, pair])
                    #print(score, pair)
                self.load()
            pair_hint_list.sort(key=lambda x:x[0], reverse=True)
            if len(pair_hint_list) > 0:
                pair_hint = pair_hint_list[0][1]
        return pair_hint

    def paint(self):
        '''绘制矩阵，初始用打印语句代替
        '''
        print(self.__bd)
        return self.__bd

    
if __name__ == '__main__':
    print("="*10, "Test Board")
    pt = Pattern()
    bd = Board(5, 6) #最好用不同的数作为两个维度，更好的测试出问题（例如两个维度颠倒）
    
    #Test init/paint
    if False:
        print("-"*10, "Test init")
        bd.paint()
        
    #Test reinit
    if False:
        print("-"*10, "Test reinit")
        bd.reinit()
        bd.paint()
        
    #Test save/load
    if False:
        print("-"*10, "Test save/load")
        bd.paint()
        bd.save()
        bd.reinit(clean_backup = False) #测试时去掉清空备份的选项
        bd.paint()
        bd.load()
        bd.paint()
        
    #Test match patterns
    if False:
        print("-"*10, "Test match")
        for color in COLOR:
            print("    Color: %s" % COLOR[color])
            bd.save()
            bd.paint()
            for cnt in bd.match(pt.get_by_name("3"), color):
                print("    Matched: %d" % cnt)  #每种pattern找到了几个（看增量，叠加在之前的上）
            bd.paint()  #退出迭代器后，应该将标记0的变化体现到原始矩阵上
            bd.load()

    #Test boom
    if False:
        print("-"*10, "Test boom")
        bd.save()
        bd.paint()
        res = bd.boom() #计算出每种格数，每种颜色，分别消除了多少次；同时把消除的格子标记0
        bd.paint()  #消除后的矩阵
        print(res)  #消除的次数（3*5矩阵表示结果）
        bd.load()
        #bd.paint()

    #Test score
    if False:
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
    if False:
        print("-"*10, "Test down")
        while bd.score(bd.boom()) == 0:
            bd.reinit(clean_backup = False) #如果碰到没有可消除的情形，临时生成新数据，并且不破坏原始备份
            bd.paint()
        bd.paint()
        for direct in DIRECT: 
            print(direct)
            bd.save()
            bd.paint()
            bd.down(DIRECT[direct])
            bd.paint()
            bd.load()

    #Test down_step
    if True:
        print("-"*10, "Test down_step")
        while bd.score(bd.boom()) == 0:
            bd.reinit(clean_backup = False) #如果碰到没有可消除的情形，临时生成新数据，并且不破坏原始备份
            bd.paint()
        bd.paint()
        for direct in DIRECT: 
            print(direct)
            bd.save()
            bd.paint()
            for _ in bd.down_step(DIRECT[direct]):
                bd.paint()
            bd.load()        
            
    #Test fill
    if False:
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
        
    #Test fill_step
    if True:
        print("-"*10, "Test fill_step")
        while bd.score(bd.boom()) == 0:
            bd.reinit(clean_backup = False) #如果碰到没有可消除的情形，临时生成新数据，并且不破坏原始备份
            bd.paint()
        bd.paint()
        for direct in DIRECT:   
            print(direct)
            bd.save()
            bd.paint()
            bd.down(DIRECT[direct])
            bd.paint()            
            for _ in bd.fill_step(DIRECT[direct]):
                bd.paint()
            bd.load()
        
    #Test swap
    if False:
        print("-"*10, "Test swap")
        bd.save()
        bd.paint()
        for a, b in [((1,1),(1,2)), ((3,2),(2,2)),((3,1),(2,2))]:
            print(bd.swap(a, b), a, b)
            bd.paint()
        bd.load()
        #bd.paint()

    #Test hint
    if False:
        print("-"*10, "Test hint")
        bd.save()
        bd.paint()
        while bd.score(bd.boom()) > 0: #自动消除，填充，直到没有可自动消除的块
            #bd.paint()
            bd.down()
            #bd.paint()
            bd.fill()
            #bd.paint()
        bd.paint()
        print(bd.hint(0))
        print(bd.hint(1))
        #bd.load() #hint函数里面已经load过了
        #bd.paint()

