#coding: utf-8

import numpy as np
import argparse
import time
import sys
import pygame
from pygame.locals import*


from board import Board
from setting import ELEMENT, COLOR, SCORE, DIRECT


FPS = 10
WINDOWWIDTH =640
WINDOWHEIGHT = 480
CELLSIZE = 80
CELLSIZE_INNER = CELLSIZE/10
CELLSIZE_SWAP = CELLSIZE/4
CELLWIDTH = 6
CELLHEIGHT = 6

assert WINDOWWIDTH >= CELLSIZE * CELLWIDTH #不会过宽
assert WINDOWHEIGHT >= CELLSIZE * CELLHEIGHT #不会过高

#RGB
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
GREY        = (185, 185, 185)
LIGHTGREY   = (205, 205, 205)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)

#Direction
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


#主函数
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Elf Board')
    
    showStartScreen()  #显示起始画面
    while True:
        runGame()    #运行游戏主体
        showGameOverScreen()    #显示游戏结束画面

#游戏主体
def runGame():
    
    get_bd = get_board()
    score_str = ""
    while True:
        direction = check_events()
        print(direction)
        
        #画背景
        BGCOLOR = BLACK
        DISPLAYSURF.fill(BGCOLOR)
        
        #画各个元素
        drawGrid() #画格子
        para = next(get_bd)
        if para[2] is not None:
            score_str = para[2]
        drawBoard(para[0], para[1], score_str)


        #更新画面
        pygame.display.update()
        FPSCLOCK.tick(FPS)


#显示开始界面
def showStartScreen():
    pass
    
#显示游戏结束画面
def showGameOverScreen():
    pass    

#======================================================================================================================
def check_events():
    direction = ""
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                direction = LEFT
            elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                direction = RIGHT
            elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                direction = UP
            elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                direction = DOWN
            elif event.key == K_ESCAPE:
                terminate()
    return direction

#游戏结束
def terminate():
    pygame.quit()
    sys.exit()

def clean_board(bd):
    '''每回合开始时，清理直到没有可以自动消除的块，但是有通过交换相邻块可以消除的块
    '''
    while True:
        #此处的boom不计算分数，刚开局以及碰到死局重开时，需要做必要的清理
        while bd.score(bd.boom()) > 0: #自动消除，填充，直到没有可自动消除的块
            bd.down()
            bd.fill()
        #寻找是否有可以消除的块
        pair = bd.hint(0) #1慢，优先消除更多分数；0快，随机消
        if not pair is None:
            break
        print("\n** DEAD **")
        bd.reinit()
    return pair

def parse(pair_input):
    pair = []
    ls = pair_input.split(',')
    #print(ls)
    if len(ls) >= 4:
         pair.append(((int)(ls[0]), (int)(ls[1])))
         pair.append(((int)(ls[2]), (int)(ls[3])))
    else:
         pair = None
    #print(pair)
    return pair

def get_board():
    bd = Board(CELLHEIGHT, CELLWIDTH)
    clean_board(bd)
    yield bd.paint(), None, None
    #time.sleep(1)
    
    #初始化轮次，分数等
    round = 0
    score = [0, 0, 0, 0, 0]
    score_c = [0, 0, 0, 0, 0]
    bonus_5 = [0, 0, 0, 0, 0]
    bonus_5_c = [0, 0, 0, 0, 0]
    bonus_4 = [0, 0, 0, 0, 0]
    bonus_4_c = [0, 0, 0, 0, 0]
    bonus_3 = [0, 0, 0, 0, 0]
    bonus_3_c = [0, 0, 0, 0, 0]

    while True:    
        #------------------------------------------------------------------------------------------------------------
        round += 1
        print("\n--------------------\nROUND %d" % round)
        pair = clean_board(bd)
        yield bd.paint(), pair, None
        time.sleep(1)
        
        print("\n.. SWAP ..")
        bd.swap(pair[0], pair[1]) #先强制用推荐值
        yield bd.paint(), pair, None
        time.sleep(1)
        
        while False: #TODO:先关掉
            pair_input = input()
            if pair_input == "":
                #无输入时，用hint算出来的推荐值
                bd.swap(pair[0], pair[1])
                break
            else:
                bd.save()
                pair = parse(pair_input)
                #输入格式正确，且交换格相邻
                if (pair != None) and (bd.swap(pair[0], pair[1]) == True):
                    #交换后，能产生消除。这里需要在判断后还原一下被写0的格子，然后交换格子的动作再执行一次（有点别扭）
                    if bd.score(bd.boom()) > 0:
                        bd.load()
                        bd.swap(pair[0], pair[1])
                        break
                bd.load()
                #bd.paint(), None
                print("\nformat as'0,0,0,1', if ignore then auto")

        print("\n-- MOVE --")
        yield bd.paint(), None, None
        #time.sleep(1)
                
        while True:
            cnt_boom = bd.boom()
            if bd.score(cnt_boom) == 0:
                break
            else:
                for i, color in enumerate(COLOR):
                    score_c[i] = bd.score(cnt_boom, color)
                    score[i] += score_c[i]
                    bonus_5_c[i] = cnt_boom[0][i]
                    bonus_5[i] += bonus_5_c[i]
                    bonus_4_c[i] = cnt_boom[1][i]
                    bonus_4[i] += bonus_4_c[i]
                    bonus_3_c[i] = cnt_boom[2][i]
                    bonus_3[i] += bonus_3_c[i]
            yield bd.paint(), None, None
            time.sleep(1)
            for _ in bd.down_step(DIRECT["DOWN"]):
                yield bd.paint(), None, None
            time.sleep(1)
            for _ in bd.fill_step(DIRECT["DOWN"]):
                yield bd.paint(), None, None
            #bd.fill()
            yield bd.paint(), None, None
            time.sleep(1)
        print("\n== DOWN ==")
        score_str = ','.join(str(i) for i in score)
        yield bd.paint(), None, score_str
        time.sleep(1)
        print("\n~~ SCORE~~")
        print(score)
        print(bonus_5)
        print(bonus_4)
        print(bonus_3)
        #------------------------------------------------------------------------------------------------------------
                

def drawGrid():
    coordinate = (0, WINDOWHEIGHT-CELLSIZE*CELLHEIGHT, CELLSIZE*CELLWIDTH, WINDOWHEIGHT) #左上右下边界坐标
    for x in range(coordinate[0], coordinate[2]+CELLSIZE, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, WHITE, (x, coordinate[1]), (x, coordinate[3]))
    for y in range(coordinate[1], coordinate[3]+CELLSIZE, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, WHITE, (coordinate[0], y), (coordinate[2], y))

def drawBoard(bd, pair=None, score=""):
    COLOR_DRAW = {0:BLACK, 1:GREY, 2:GREEN, 3:YELLOW, 4:BLUE, 5:RED}
    COLOR_INNER_DRAW = {0:BLACK, 1:LIGHTGREY, 2:LIGHTGREEN, 3:LIGHTYELLOW, 4:LIGHTBLUE, 5:LIGHTRED}

    print(bd)
    #print(pair)

    coordinate = (0, WINDOWHEIGHT-CELLSIZE*CELLHEIGHT, CELLSIZE*CELLWIDTH, WINDOWHEIGHT) #左上右下边界坐标
    row, col = bd.shape[0], bd.shape[1]

    for i in range(row):
        for j in range(col):
            CellRect = pygame.Rect(coordinate[0]+j*CELLSIZE+1, coordinate[1]+i*CELLSIZE+1, CELLSIZE-2, CELLSIZE-2)
            pygame.draw.rect(DISPLAYSURF, COLOR_DRAW[bd[i][j]], CellRect)
            CellInnerRect = pygame.Rect(coordinate[0]+j*CELLSIZE+CELLSIZE_INNER, coordinate[1]+i*CELLSIZE+CELLSIZE_INNER, CELLSIZE-CELLSIZE_INNER*2, CELLSIZE-CELLSIZE_INNER*2)
            pygame.draw.rect(DISPLAYSURF, COLOR_INNER_DRAW[bd[i][j]], CellInnerRect)
            
    if pair is not None:
        for cellSwap in pair:
            CellSwapRect = pygame.Rect(coordinate[0]+cellSwap[1]*CELLSIZE+CELLSIZE_SWAP, coordinate[1]+cellSwap[0]*CELLSIZE+CELLSIZE_SWAP, CELLSIZE-CELLSIZE_SWAP*2, CELLSIZE-CELLSIZE_SWAP*2)
            pygame.draw.rect(DISPLAYSURF, WHITE, CellSwapRect)
            
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    textSurfaceObj = BASICFONT.render(score, True, GREEN, BLUE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (480+100, 150)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        

if __name__ == '__main__':
    main()
 
