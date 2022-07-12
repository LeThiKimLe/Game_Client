
import pygame 
import button
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(main_dir, '..'))

load_file=lambda filename:os.path.join(main_dir, 'data', filename)
width,height =800,700
blue = (0, 0, 128)
a=[]
b=[]
c=['You must find the answers to the questions',' hidden behind the objects in order to win','and level up in the shortest amount of time.',
'if you complete the challenge less than 60 sec',' you will be rewarded with extra score ','otherwise your score will be deducted.',
'If you answer all the questions incorrectly',' you will lose']
pygame.init()
screen = pygame.display.set_mode((width,height))
bg_img = pygame.image.load(load_file('im_help.png'))
bg_img = pygame.transform.scale(bg_img,(width,height))
font = pygame.font.Font('freesansbold.ttf', 18)
def label(x,y,infofation):

    a=[]
    b=[]
    i=0
    while i<8:
        text = font.render(infofation[i], True, blue, None)
        textRect = text.get_rect()
        textRect.center = (x,y)
        a.append(text)
        b.append(textRect)
        y+=40
        i+=1
    return a,b
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
    for i in range(8):
        a,b=label(380,200,c)
    while run:
        screen.fill([255,255,255])    
        pygame.Surface.set_colorkey(bg_img,[0,0,0])
    
        screen.blit(bg_img,(0,0))
        for i in range(8):
            screen.blit(a[i],b[i])
            
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
    
