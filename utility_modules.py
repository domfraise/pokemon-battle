# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 20:47:59 2016

@author: Dom
"""

#Utility function

import pygame
screen_width = 640*2
screen_height = 360*2
screen=pygame.display.set_mode((screen_width,screen_height))   #set window size
pygame.display.set_caption("Pokemon")

def blit_background():

    background = pygame.image.load("battlebackground.jpeg")
    background = pygame.transform.smoothscale(background,(screen_width,screen_height))
    screen.blit(background,(0,0))