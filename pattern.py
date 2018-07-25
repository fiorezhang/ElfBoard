#coding: utf-8

import numpy as np

class Pattern():
    def __init__(self):
        '''生成五连，五折，四条，四块，三条的5*5 pattern
        '''
        self.__pt_5_l = np.zeros((2, 5, 5), np.int) #五连
        self.__pt_5_l[0] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [1,1,1,1,1],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_l[1] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0]]

        self.__pt_5_b = np.zeros((4, 5, 5), np.int) #五折
        self.__pt_5_b[0] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_b[1] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,1,1],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_b[2] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,1,1,1],
                            [0,0,1,0,0],
                            [0,0,1,0,0]]
        self.__pt_5_b[3] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0]]

        self.__pt_4_l = np.zeros((2, 5, 5), np.int) #四连
        self.__pt_4_l[0] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [1,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_4_l[1] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0]]

        self.__pt_4_s = np.zeros((1, 5, 5), np.int) #四块
        self.__pt_4_s[0] = [[0,0,0,0,0],
                            [0,1,1,0,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]

        self.__pt_3_l = np.zeros((2, 5, 5), np.int) #三连
        self.__pt_3_l[0] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_3_l[1] = [[0,0,0,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0]]

        self.__pt_all = np.concatenate((self.__pt_5_l, self.__pt_5_b), axis=0)
        self.__pt_all = np.concatenate((self.__pt_all, self.__pt_4_l), axis=0)
        self.__pt_all = np.concatenate((self.__pt_all, self.__pt_4_s), axis=0)
        self.__pt_all = np.concatenate((self.__pt_all, self.__pt_3_l), axis=0)
    
    def get_all(self):
        return self.__pt_all

    def get_5_l(self):
        return self.__pt_5_l

    def get_5_b(self):
        return self.__pt_5_b

    def get_4_l(self):
        return self.__pt_4_l

    def get_4_s(self):
        return self.__pt_4_s

    def get_3_l(self):
        return self.__pt_3_l


if __name__ == '__main__':
    pt = Pattern()
    print(pt.get_all())
    print(pt.get_5_l())
    print(pt.get_5_b())
    print(pt.get_4_l())
    print(pt.get_4_s())
    print(pt.get_3_l())
