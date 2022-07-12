
import pygame 
import Module.button as button
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(main_dir, '..'))

load_file=lambda filename:os.path.join(main_dir, 'data', filename)

width,height =800,700
blue = (0, 0, 128)
red=(255,0,0)
pygame.init()
screen = pygame.display.set_mode((width,height))
bg_img = pygame.image.load(load_file('bgthongbaoo.jpg'))
bg_img = pygame.transform.scale(bg_img,(width,height))
font = pygame.font.Font('freesansbold.ttf', 30)
def label(x,y,infofation):
    text = font.render(infofation, True, red, None)
    textRect = text.get_rect()
    textRect.center = (x,y)
    return text,textRect

a,b=label(380,230,'Account registration failed')
c,d=label(230,280,'Please check: ')
e,f=label(400,340,'1.Username and PasWord must not null')
g,h=label(310,420,'2.Username already exists')
g1,h1=label(400,480,'-> you must enter another Username')
##button
def resize(image,scale):
    x=image.get_width()
    y=image.get_height()
    image =pygame.transform.scale(image, (x*scale, y*scale))
    return image
ok_img = pygame.image.load(load_file('ok1.png')).convert_alpha()
ok_img=resize(ok_img,0.6)
ok_button=button.Button(400,630,ok_img, 0.8)
def main():
    run = True
    while run:
    
            

        screen.blit(bg_img,(0,0))
        screen.blit(a,b)
        screen.blit(c,d)
        screen.blit(e,f)
        screen.blit(g,h)
        screen.blit(g1,h1)



    
            
        if ok_button.draw(screen):
            run=False
       

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False
            
        pygame.display.update()

if __name__ == '__main__':
    main()
    pygame.quit()
    
