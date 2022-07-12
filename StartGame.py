
import Module.thongbao as thongbao 
import Module.thongbao1 as thongbao1
import Module.thongbao3 as thongbao3
import pygame as pg
import Module.inputbox as inputbox
import Module.button as button
import GameMenu
from Module.ConnectServer import *
import os

width=800
height=700
ID=''
pg.init()
screen = pg.display.set_mode((width,height))

main_dir = os.path.split(os.path.abspath(__file__))[0]
load_file=lambda filename:os.path.join(main_dir, 'data', filename)

bg_img = pg.image.load(load_file('bglogin.webp'))
bg_img = pg.transform.scale(bg_img,(width,height))

FONT = pg.font.Font(None, 40)
font = pg.font.Font('freesansbold.ttf', 32)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
login_img = pg.image.load(load_file('login1.png')).convert_alpha()
reg_img = pg.image.load(load_file('dangki1.png')).convert_alpha()

def label(x,y,infofation):
    text = font.render(infofation, True, blue, None)
    textRect = text.get_rect()
    textRect.center = (x,y)
    return text,textRect

def resize(image,scale):
    x=image.get_width()
    y=image.get_height()
    image = pg.transform.scale(image, (x*scale, y*scale))
    return image
     
login_img =resize(login_img,0.5)
reg_img =resize(reg_img,0.6)
a,b=label(300,440,'UserName')   
c,d=label(300,500,'PassWord')

login_button = button.Button(250, 550, login_img, 0.8)
reg_button = button.Button(400, 550,reg_img, 0.8)
##Hàm đăng nhập

def login(username,password):
    n=username.text
    p=password.text
    id=""
    infor=[n,p]
    check_user, id =Request_Server('LOGIN', infor) 
    global ID
    ID=id
    return check_user
    #return True
    
def  registration(username,password):
    global ID
    n=username.text
    p=password.text
    if n=="" or p=="":
        return False

    infor=[n,p]
    add_user, ID =Request_Server('REGIS', infor) 
    return add_user
		
input_box1 = inputbox.InputBox(385, 420, 140, 40)
input_box2 = inputbox.InputBox(385, 480, 140, 40)
input_boxes = [input_box1, input_box2]   

def main():

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
                
        screen.blit(bg_img,(0,0))
        if login_button.draw(screen):
            if login(input_box1,input_box2):
                Request_Server('GET_DATA')
                while(GameMenu.exit==0):
                    GameMenu.main(input_box1.text, ID)
                return
            else:
                input_box1.text=''
                input_box1.txt_surface= FONT.render(input_box1.text, True, input_box1.color)
                input_box2.text=''
                input_box2.txt_surface= FONT.render(input_box2.text, True, input_box2.color)
                thongbao.main()

        elif reg_button.draw(screen):
            if registration(input_box1,input_box2):
                thongbao1.main()
            else:
                input_box1.text=''
                input_box1.txt_surface= FONT.render(input_box1.text, True, input_box1.color)
                input_box2.text=''
                input_box2.txt_surface= FONT.render(input_box2.text, True, input_box2.color)
                thongbao3.main()
        screen.blit(a, b)
        screen.blit(c, d)
        for box in input_boxes:
            box.draw(screen)
        pg.display.flip()

if __name__ == '__main__':
    main()