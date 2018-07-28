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

        self.__pt_5_v = np.zeros((4, 5, 5), np.int) #五折
        self.__pt_5_v[0] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_v[1] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,1,1],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_v[2] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,0,1,1,1],
                            [0,0,1,0,0],
                            [0,0,1,0,0]]
        self.__pt_5_v[3] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0]]

        self.__pt_5_t = np.zeros((4, 5, 5), np.int) #五T
        self.__pt_5_t[0] = [[0,0,0,0,0],
                            [0,0,1,0,0],
                            [1,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_t[1] = [[0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_t[2] = [[0,0,0,0,0],
                            [0,0,1,0,0],
                            [0,0,1,1,1],
                            [0,0,1,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_t[3] = [[0,0,0,0,0],
                            [0,0,0,0,0],
                            [0,1,1,1,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0]]

        self.__pt_5_x = np.zeros((1, 5, 5), np.int) #五X
        self.__pt_5_x[0] = [[0,0,0,0,0],
                            [0,0,1,0,0],
                            [0,1,1,1,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0]]

        self.__pt_5_p = np.zeros((8, 5, 5), np.int) #五P
        self.__pt_5_p[0] = [[0,0,0,0,0],
                            [0,1,1,0,0],
                            [1,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[1] = [[0,0,0,0,0],
                            [1,1,1,0,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[2] = [[0,1,0,0,0],
                            [0,1,1,0,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[3] = [[0,0,1,0,0],
                            [0,1,1,0,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[4] = [[0,0,0,0,0],
                            [0,1,1,1,0],
                            [0,1,1,0,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[5] = [[0,0,0,0,0],
                            [0,1,1,0,0],
                            [0,1,1,1,0],
                            [0,0,0,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[6] = [[0,0,0,0,0],
                            [0,1,1,0,0],
                            [0,1,1,0,0],
                            [0,0,1,0,0],
                            [0,0,0,0,0]]
        self.__pt_5_p[7] = [[0,0,0,0,0],
                            [0,1,1,0,0],
                            [0,1,1,0,0],
                            [0,1,0,0,0],
                            [0,0,0,0,0]]
                            
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

        self.__pt_4_o = np.zeros((1, 5, 5), np.int) #四块
        self.__pt_4_o[0] = [[0,0,0,0,0],
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

        self.__pt_5 = np.concatenate((self.__pt_5_l, self.__pt_5_v), axis=0)
        self.__pt_5 = np.concatenate((self.__pt_5, self.__pt_5_t), axis=0)
        self.__pt_5 = np.concatenate((self.__pt_5, self.__pt_5_x), axis=0)
        self.__pt_5 = np.concatenate((self.__pt_5, self.__pt_5_p), axis=0)
        
        self.__pt_4 = np.concatenate((self.__pt_4_l, self.__pt_4_o), axis=0)
        
        self.__pt_3 = self.__pt_3_l
        
        self.__pt_all = np.concatenate((self.__pt_5, self.__pt_4), axis=0)
        self.__pt_all = np.concatenate((self.__pt_all, self.__pt_3), axis=0)
    
    def get_all(self):
        return self.__pt_all
        
    def get_5(self):
        return self.__pt_5
        
    def get_4(self):
        return self.__pt_4
        
    def get_3(self):
        return self.__pt_3

    def get_by_name(self, name="all"):
        if name == "all":
            return self.get_all()
        elif name == "5":
            return self.get_5()
        elif name == "4":
            return self.get_4()
        elif name == "3":
            return self.get_3()
        else:
            return None

if __name__ == '__main__':
    print("="*10, "Test Pattern")
    pt = Pattern()
    

    # Test get_xxx
    if True:
        print("-"*10, "Test get_xxx")
        print("."*10)
        print(pt.get_all())
        print("."*10)
        print(pt.get_5())
        print("."*10)
        print(pt.get_4())
        print("."*10)
        print(pt.get_3())
        
    # Test get_by_name
    if True:
        print("-"*10, "Test get_by_name")
        print("."*10)
        print(pt.get_by_name())
        print("."*10)
        print(pt.get_by_name("5"))
        print("."*10)
        print(pt.get_by_name("4"))
        print("."*10)
        print(pt.get_by_name("3"))
        print("."*10)
        print(pt.get_by_name(""))
        