
import pygame
import Module.button as button
from tkinter import *  
import os
import Module.StatisticsWin as StatisticsWin

main_dir = os.path.split(os.path.abspath(__file__))[0]
load_file=lambda filename:os.path.join(main_dir, 'data', filename)

def resize(image,scale):
    x=image.get_width()
    y=image.get_height()
    image = pygame.transform.scale(image, (x*scale, y*scale))
    return image

def initial():

    global width, height, screen, bg_img, ID, help_img, oneplayer_img, statics_img, user_img, exit_img, user, red, help_button, oneplayer_button, exit_button, statics_button
    width,height =800,700
    screen = pygame.display.set_mode((width,height))
    bg_img = pygame.image.load(load_file('anhnen2.WEBP'))
    bg_img = pygame.transform.scale(bg_img,(width,height))
    ID=''
    help_img = pygame.image.load(load_file('help2.png')).convert_alpha()
    oneplayer_img = pygame.image.load(load_file('play2.png')).convert_alpha()
    exit_img = pygame.image.load(load_file('exit2.png')).convert_alpha()
    statics_img = pygame.image.load(load_file('thongke2.png')).convert_alpha()
    user_img=pygame.image.load(load_file('user.png')).convert_alpha()
    user=""

    user_img=resize(user_img,0.2)
    help_img =resize(help_img,0.6)
    oneplayer_img =resize(oneplayer_img,0.6)
    exit_img =resize(exit_img,0.6)
    statics_img =resize(statics_img,0.65)
    red=(255,0,0)

    help_button = button.Button(300, 300, help_img, 0.8)
    oneplayer_button = button.Button(300, 350, oneplayer_img, 0.8)
    exit_button = button.Button(300, 460, exit_img, 0.8)
    statics_button = button.Button(300, 400, statics_img, 0.8)
        
def label(x,y,infofation):
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render(infofation, True, red, None)
    textRect = text.get_rect()
    textRect.center = (x,y)
    return text,textRect

#create button instances

exit=0

def main(x, userID):

    global exit
    pygame.init()
    initial()

    a,b=label(100,140,x)
    run = True
    while run:

        screen.blit(bg_img,(0,0))
        screen.blit(user_img,(80,30))
        screen.blit(a,b)
    
        if help_button.draw(screen):
            print('Help')
        elif oneplayer_button.draw(screen):
            import MainGame
            MainGame.main(userID)
            run=False

        elif exit_button.draw(screen):
            exit=1
            run=False
            
        elif statics_button.draw(screen):
            StatisticsWin.run_statis()
            run=False

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False
                exit=1

        pygame.display.update()
    pygame.quit()
    
def run(name, id):
    main(name, id)


