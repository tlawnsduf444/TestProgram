#!/usr/bin/env python

import datetime
import time
import pygame
import os

class Capture:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    pad_size = [0, 0]
    cnt = 0
    pos = list()
    data = []

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('screen_test')
        self.screen = pygame.display.set_mode(self.pad_size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.resolution = self.screen.get_size()

    def runCapture(self):
        runflag = True

        while runflag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runflag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        runflag = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos.append(pygame.mouse.get_pos())
                    self.data.append(str(self.cnt + 1) + '\t' + str(self.pos[self.cnt][0]) + '\t' + str(self.pos[self.cnt][1]) + '\n')
                    self.cnt += 1

            self.screen.fill(self.WHITE)
            self.drawtext()
            self.drawObject()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def drawtext(self):
        font = pygame.font.SysFont(None, 40)
        text1 = font.render('CLICK : ' + str(self.cnt), True, self.BLACK)
        if self.cnt == 0:
            text2 = font.render('POS : None', True, self.BLACK)
        else:
            text2 = font.render('POS : ' + str(self.pos[self.cnt - 1]), True, self.BLACK)

        self.screen.blit(text1,(0,0))
        self.screen.blit(text2,(200,0))

    def drawObject(self):
        for i in range(len(self.pos)):
            pygame.draw.circle(self.screen, self.RED, self.pos[i], 25)

    def write(self):
        with open(os.getcwd() + "/screen_file/" + str(datetime.datetime.now()), 'w') as cap:
            cap.writelines(self.data)

if __name__ == "__main__":
    start = Capture()
    start.runCapture()
    if not os.path.exists(os.getcwd() + "/screen_file"):
        os.makedirs(os.getcwd() + "/screen_file")
    start.write()