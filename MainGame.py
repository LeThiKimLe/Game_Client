
from multiprocessing.connection import wait
import pygame as pg
from pygame.locals import *
import os
import Module.data_exec as de
from time import sleep
import math
from datetime import date 
import Module.file_action as fileac
from Module.ConnectServer import *
from Module.Ultility import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
SCREENRECT = pg.Rect(0, 0, 1000, 700)
all = pg.sprite.RenderUpdates()
clock = pg.time.Clock()
SCORE=0
COUNTER=0
GOAL=200
RESULT=False
ID=''

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
        surface = scale(surface, 0.8)
        pg.Surface.set_colorkey(surface, [0,0,0])
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()

def load_character(img1, num):
    nv=[]
    base=str(os.path.basename(img1))
    file=base.split('.')
    width=[]
    height=[]

    for i in range(1,num+1):
        file_name = os.path.join(main_dir, "data", file[0][:-1]+str(i)+'.'+file[1])
        nv.append(load_image(file_name))
        pg.Surface.set_colorkey (nv[-1], [0,0,0])
    return nv

def scale(surface,scale_in):
    x=surface.get_width()
    y=surface.get_height()
    surface = pg.transform.scale(surface, (x*scale_in, y*scale_in))
    return surface



def load_question():

    def load_multichoices(Ques):
        df=de.get_multichoices(Ques)
        return list(df.iloc[0][1:].values)

    ques_table=de.get_question()
    pick=ques_table.sample()
    question= pick['Question'].iloc[0]
    quesID= pick['QuesID'].iloc[0]
    level= pick['QuesLevel'].iloc[0]
    choices=load_multichoices(quesID.strip())
    return quesID, [question, choices, level]

def load_answer(Ques):
        return(de.get_answer(Ques.strip()))

class Transfer_surface():

    def __init__(self, screen):
        self.surface=pg.Surface([SCREENRECT.width, SCREENRECT.height], SRCALPHA)
        self.des_screen=screen
        self.alpha=0

    def Fade_out(self):
        
        self.surface.set_alpha(self.alpha)
        self.surface.fill((0,0,0))
        while self.alpha<100:
            self.alpha+=1
            self.surface.set_alpha(self.alpha)
            self.des_screen.blit(self.surface, (0, 0))
            pg.display.update()
            pg.time.delay(30)


class Player(pg.sprite.Sprite):
    """Representing the player as a moon buggy type car."""

    speed = 10
    bounce = 24
    gun_offset = -11
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=SCREENRECT.topleft)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1
        self.collision=0
        
        self.dir={1: (-20, 0), 2: (20, 0), 3: (0, -20), 0: (0, 20)}
        self.player_mask = pg.mask.from_surface(self.image)
    
    def moved(self, direction):
        self.next_step=self.rect.move(self.dir[direction])
        if self.collision==0:
            self.rect.move_ip(self.dir[direction])
        self.rect = self.rect.clamp(SCREENRECT)
        if direction == 0:
            self.image = self.images[0]
        elif direction==1:
            self.image = self.images[1]
        elif direction==2:
            self.image = self.images[2]
        elif direction==3:
            self.image = self.images[3]
        self.next=self.rect

    def tieptheo(self, direction):

        self.next=self.rect.move(self.dir[direction])
        return self.next
        
    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top

class Static_Object(pg.sprite.Sprite):

    images = []

    def __init__(self, image_in, pos_in):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.images=image_in
        self.image = image_in[0]
        self.rect = self.image.get_rect(topleft=pos_in)
        self.frame = 0
        self.finish=False

    def chosen(self):
        self.image=self.images[1]

    def unchosen(self):
        self.image=self.images[0]

class wall(pg.sprite.Sprite):

    images = []

    def __init__(self, pos_in):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image("wall1.png")
        self.image = scale(self.image, 0.25)
        self.rect = self.image.get_rect(topleft=pos_in)
        self.frame = 0

class Question(pg.sprite.Sprite):

    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image("note.png")
        self.image = scale(self.image, 2)
        self.rect = self.image.get_rect(center=SCREENRECT.center)
        pg.Surface.set_colorkey (self.image, [0,0,0])
        self.contain_text = pg.sprite.Group()
        self.contain_choice = pg.sprite.Group()

        Choices.containers=self.contain_choice
        Ques_Content.containers=self.contain_text
        self.question=Ques_Content(self.rect)
        self.list_choices_image= [load_image('choice11.png'), load_image('choice21.png'), load_image('choice31.png')]

    def get_content(self):
        self.group_choice=pg.sprite.Group()
        self.quesID, msg=load_question()
        self.plus=msg[-1]
        first_pos=self.rect.midleft
        
        self.question.get_text(msg[0], msg[2])
        for i in range(len(msg[1])):
            choice=Choices(self.list_choices_image[i], (first_pos[0]+180*i,first_pos[1]), i)
            choice.get_choices(msg[1][i])
            self.group_choice.add(choice)
        

        submit=Choices(load_image('submit.png'),(self.rect.centerx-50, self.rect.centery+130), 3, 1/2)
        submit.get_choices("")
        self.group_choice.add(submit)

        self.contain_text.draw(self.image)
        self.contain_choice.draw(self.image)

class Text_Content(pg.sprite.Sprite):

    def __init__(self, pos_in=(10,10)):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = pg.font.SysFont('chalkduster.ttf', 35)
        self.font.set_italic(1)
        self.color = "red"
        self.image = self.font.render("hello", 0, self.color)
        self.rect = self.image.get_rect(center=pos_in)
        self.content="Content"

    def update(self):
        self.image = self.font.render(self.content, 0, self.color)

    def get_text(self, text):
        self.content=text
        self.update()

class Ques_Content(pg.sprite.Sprite):

    def __init__(self, parent_rect):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.rect=parent_rect
        self.pos_in= (self.rect.x-80, int(self.rect.centery/3))
        self.image = pg.Surface(parent_rect.size, SRCALPHA)
        self.contain=pg.sprite.Group()
        Text_Content.containers=self.contain
        
    def get_text(self, text, plusgrade):
        list_word=text.split()
        first=0
        for i in range(0,len(list_word)):
            if (i+1)%6==0 or i==len(list_word)-1:
                text_split=' '.join(list_word[first:i+1])
                first=i+1
                newSprite=Text_Content(self.pos_in)
                newSprite.get_text(text_split)
                self.pos_in=(self.pos_in[0], self.pos_in[1]+50)

        grade=Text_Content((self.rect.topleft[0]+310, self.rect.topleft[1]+5))
        grade.color='yellow'
        grade.get_text('+'+str(plusgrade*100)+'đ')

        print_ques = self.contain.draw(self.image)


class Grade_Content(pg.sprite.Sprite):

    def __init__(self, pos_in):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('grade.png')
        self.image = scale(self.image, 1/15)
        self.rect = self.image.get_rect(topleft=pos_in)
        self.contain=pg.sprite.Group()
        Text_Content.containers=self.contain
        
    def get_text(self, grade):
    
        self.text=Text_Content((self.rect.centerx, self.rect.centery))
        self.text.color='yellow'
        self.text.get_text('+'+str(grade))
        print_grade = self.contain.draw(self.image)


class Choices(pg.sprite.Sprite):

    def __init__(self, image_in, pos_in, index, scale_in=1.0):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image=image_in
        self.image=scale(self.image, scale_in)
        self.rect = self.image.get_rect(topleft=pos_in)
        self.pos=pos_in
        self.chose=False
        self.contain_da = pg.sprite.GroupSingle()
        Text_Content.containers=self.contain_da, self.containers
        self.starpos=(self.rect.topleft[0]+150, self.rect.topleft[1]+70)
        self.check_pos=(self.starpos[0]+110, self.starpos[1])
        self.index=index

    def get_choices(self, choice):
        self.noidung=choice
        self.text=Text_Content((self.rect.centerx, self.rect.centery))
        self.text.color='yellow'
        self.text.get_text(choice)
        print_choice = self.contain_da.draw(self.image)
        

class Blur(pg.sprite.Sprite):
    images = []
    chosen=False

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = pg.Surface([SCREENRECT.width, SCREENRECT.height])
        self.image.set_alpha(230)
        self.image.fill((192,192,192))
        self.rect = SCREENRECT
        self.contain_ques = pg.sprite.Group()
        Question.containers=self.contain_ques
        Mouse.containers=self.contain_ques
        self.load_quizz()

    def load_quizz(self):
        self.quizz=Question()
        self.quizz.get_content()
        print_quizz = self.contain_ques.draw(self.image)

    def update(self):
        if self.chosen==True:
            self.contain_ques.draw(self.image)

    def Check_ans(self):
        pass



class Maze:
    def __init__(self):
       self.M = 500
       self.N = 350
       self.surface=pg.Surface(SCREENRECT.size, SRCALPHA)
       
    def draw_maze(self, screen):
        global group_wall
        group_wall = pg.sprite.Group()
        wall.containers=group_wall

        local_dict1={250:[[0, 250], [350, 580], [670, 700]],
                    400:[[0, 50], [150, 250], [350, 600]],
                    600:[[70, 250],[600, 620]],
                    770:[[80, 250], [550, 670]],
                    620:[[550, 600]]}
        local_dict2={250: [[60, 250], [400, 600], [770, 940]],
                     350: [[0, 100], [200, 250], [400, 500], [600, 710],[800, 1000] ],
                     550:[[0, 150], [770, 900]],
                     600:[[520, 620]]
        }
        
        for x in local_dict1.keys():
            for y_period in local_dict1[x]:
                for y in range(y_period[0], y_period[1], 20):
                    wall((x, y))

        for y in local_dict2.keys():
            for x_period in local_dict2[y]:
                for x in range(x_period[0], x_period[1], 20):
                    wall((x,y))

        group_wall.update()
        draw_maze = group_wall.draw(self.surface)
        global maze_mask
        maze_mask = pg.mask.from_surface(self.surface)
        screen.blit(self.surface, (0, 0))
        pg.display.update()
        return self.surface

class Hightlight(pg.sprite.Sprite):
    def __init__(self, pos_in, index):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image("star.png")
        self.image = scale(self.image, 1/10)
        pg.Surface.set_colorkey(self.image, [0,0,0])
        self.rect = self.image.get_rect(topleft=pos_in)
        self.index=index

class Check_Answer(pg.sprite.Sprite):

    def __init__(self, pos_in, check):
            pg.sprite.Sprite.__init__(self, self.containers)
            self.true = load_image("true.png")
            self.false=load_image('false.png')
            self.image=self.true
            if check==False:
                self.image=self.false
            self.image = scale(self.image, 1/4)
            pg.Surface.set_colorkey(self.image, [0,0,0])
            self.rect = self.image.get_rect(topleft=pos_in)
            self.check=check
            
class Score(pg.sprite.Sprite):
    """to keep track of the score."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = pg.font.Font(None, 30)
        self.font.set_italic(1)
        self.color = "red"
        self.lastscore = -1
        self.image = self.font.render(str(SCORE), 0, self.color)
        self.rect = self.image.get_rect(topleft=SCREENRECT.topleft)

    def update(self):
        """We only update the score in update() when it has changed."""
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)

class Timer(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = pg.font.Font(None, 30)
        self.font.set_italic(1)
        self.color = "black"
        self.lastsec = 0
        self.lastmin=0
        self.image = self.font.render('Time: 00:00', 0, self.color)
        self.rect = self.image.get_rect(topleft=(SCREENRECT.topleft[0]+100, SCREENRECT.topleft[1]))

    def update(self):
        """We only update the score in update() when it has changed."""
        sec=math.floor(COUNTER)
        if sec!=self.lastsec:
            min=sec//60
            sec=sec%60
            if min<10: 
                min_in='0'+str(min)
            else:
                min_in=str(min)
            if sec<10:
                sec_in='0'+str(sec)
            else:
                sec_in=str(sec)
            self.lastsec=sec
            self.lastmin=min
            msg = "Time: %s:%s" % (min_in,sec_in)
            self.image = self.font.render(msg, 0, self.color)


class Mouse(pg.sprite.Sprite):

    images = []
    limit= SCREENRECT

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('mouse_click.png')
        pg.Surface.set_colorkey(self.image, [0,0,0])
        self.image=pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=SCREENRECT.center)
        self.frame = 0
    
    def update(self):
        mouse_pos = pg.mouse.get_pos()
        w, h = self.image.get_size()
        topleft=(mouse_pos[0] - w / 2, mouse_pos[1])
        if (self.limit.topleft[0]+80<topleft[0]<self.limit.topleft[0]+self.limit.width-50 and self.limit.topleft[1]+100<topleft[1]<self.limit.topleft[1]+self.limit.height-70):
            self.rect.topleft=topleft

class Treasure_Hunt():
   
    def __init__(self):
        global RESULT
        self.screen = self.init_pygame()
        self.decorate_logo()
        self.create_background()
        self.put_object()
        RESULT=self.put_character()
        trans=Transfer_surface(self.screen)
        trans.Fade_out()
        self.finishLevel(RESULT)
      
        
    def decorate_logo(self):
        # decorate the game window
        icon = pg.transform.scale(load_image('logo.png'), (32, 32))
        pg.display.set_icon(icon)
        pg.display.set_caption("Pygame Aliens")
        pg.mouse.set_visible(0)

    def init_pygame(self):
        # Initialize pygame
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()
        
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None
        global winstyle
        global bestdepth

        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        return screen


    def create_background(self):
        image = load_image("co2.jpg")
    
        self.background = pg.Surface(SCREENRECT.size)

        for x in range(0, SCREENRECT.height, image.get_height()):
            self.background.blit(image, (0,x))
            for y in range(0, SCREENRECT.width, image.get_width()):
                self.background.blit(image, (y,x))

        maze=Maze()
        self.background.blit(maze.draw_maze(self.screen), (0,0))
        self.screen.blit(self.background, (0, 0))

        pg.display.flip()


    def put_character(self):
        global COUNTER
        start_ticks=pg.time.get_ticks() #starter tick

        global SCORE
        fullscreen = False
        Player.containers = all

        Player.images = load_character("c1.png",4)
        global player
        player = Player()
        i=0
        flag=0
        run=True
        direction=0

        Question.containers=all
        Mouse.containers=all

        Score.containers=all
        Timer.containers=all
        
        self.mouse=Mouse()

        Blur.containers=all
        blur=pg.sprite.Sprite()
        chose=pg.sprite.Sprite()
        check=pg.sprite.Sprite()
        cur_item=pg.sprite.Sprite()
        pos=(0,0)
        group_checkans=pg.sprite.Group()
        group_finishItem=pg.sprite.Group()
        Hightlight.containers=all
        Check_Answer.containers=all, group_checkans
        has_submitted=False
        right_ans=False
        score=Score()
        timer=Timer()
        while run:
            if SCORE>=GOAL:
                return True
            COUNTER=(pg.time.get_ticks()-start_ticks)/1000 
            pg.display.update()
            for event in pg.event.get():
                if event.type==KEYDOWN:
                    if event.unicode == "q":
                        return False

                if event.type == pg.MOUSEBUTTONDOWN:
                        pos = pg.mouse.get_pos()
                else:
                    pos=(0,0)
            
            keys = pg.key.get_pressed()
            
            all.clear(self.screen,self.background)
            all.update()
            
            if(flag==0):
                if keys[pg.K_LEFT]==1:
                    direction=1
                    self.Check_collision(direction)
                    player.moved(direction)

                if keys[pg.K_RIGHT]==1:
                    direction=2
                    self.Check_collision(direction)
                    player.moved(direction)

                if keys[pg.K_UP]==1:
                    direction=3
                    self.Check_collision(direction)
                    player.moved(direction)

                if keys[pg.K_DOWN]==1:
                    direction=0 
                    self.Check_collision(direction)
                    player.moved(direction)

            if keys[pg.K_SPACE]==1:
                if count!=0 and flag==0:
                    right_ans=False
                    blur=Blur()
                    self.mouse=Mouse()
                    self.mouse.limit=blur.quizz.rect
                    blur.contain_ques.draw(blur.image)
                    blur.contain_ques.update()
                    flag=1
                
            if keys[pg.K_b]==1:
                if(flag==1):
                    flag=0
                    self.mouse.limit=SCREENRECT
                    chose.kill()
                    for spr in group_checkans:
                        spr.kill()
                    if right_ans==True:
                        SCORE+=blur.quizz.plus*100
                    blur.kill()
                    if has_submitted==True:
                        group_finishItem.add(cur_item)
                        has_submitted=False
                
            if(flag==1 and blur.alive()):
                if has_submitted==False:
                    pos=(pos[0]-120, pos[1]-50)
                    clicked_sprites = [s for s in blur.quizz.group_choice if s.rect.collidepoint(pos)]
                
                    for sp in clicked_sprites:
                        if (sp.noidung!=""):
                            chose.kill()
                            chose=Hightlight(sp.starpos, sp.index)
                        else:
                            has_submitted=True
                            ans=load_answer(blur.quizz.quesID)
                            for s in blur.quizz.group_choice:
                                if s!=sp:
                                    check=Check_Answer(s.check_pos, s.noidung==ans)
                                    if check.check==True:
                                        if s.index==chose.index:
                                            right_ans=True

                clicked_sprites.clear()
                blur.contain_ques.draw(blur.image)
                blur.contain_ques.update()

            count=0
            for item in self.object:
                if item in pg.sprite.spritecollide(player, self.object, 0) and item not in group_finishItem:
                    item.chosen()
                    cur_item=item
                    count=count+1
                else:
                    item.unchosen()
            if len(self.object.sprites())==len(group_finishItem.sprites()):
                return False
            
            all.update()
            dirty = all.draw(self.screen)
            pg.display.update(dirty)
            clock.tick(20)
    
    def Check_collision(self,direction):

        next=player.tieptheo(direction)
        offset=(next.x, next.y)
        if  maze_mask.overlap(player.player_mask, offset):
            player.collision=1
        else:
            player.collision=0

    def put_object(self):

        list_position=[(503, 88), (0, 600), (467, 432), (820, 125), (50, 400), (810, 580), (170, 116)]
        list_image=['rao1.png', 'nam1.png', 'nuoc1.png', 'cat1.png', 'rock1.png', 'chau1.png', 'den1.png']
        self.object = pg.sprite.Group()
        Static_Object.containers = self.object, all
        for i in range(7):
            Static_Object(load_character(list_image[i],2), list_position[i])
            i+=1
        all.update()
        dirty = all.draw(self.screen)
        pg.display.update(dirty)

    def finishLevel(self,result):

        if result==True:
            kq='WIN'
        else:
            kq='LOSE'
        data = {'Result':kq,
            'Score': SCORE,
            'Bonus': int(60-COUNTER),
            'Total score':SCORE+int(60-COUNTER),
            }
        
        surface=load_image('sky.jpg')
        surface=pg.transform.scale(surface, SCREENRECT.size)
    
        result_rolls=load_image('rolll.png')
        result_rolls=scale(result_rolls, 0.2)
        pg.Surface.set_colorkey(result_rolls,[255,255,255])
        score=load_image('score_win.png')
        if result==False:
            score=load_image('score_lose.png')
        result_rolls.blit(score, (result_rolls.get_rect().topleft[0]+250, result_rolls.get_rect().topleft[1]+200))
        surface.blit(result_rolls, (100,0))
        self.screen.blit(surface, (0,0))
        pg.display.update()
        confirm=False
        group_result=pg.sprite.Group()
        Text_Content.containers=group_result
        
        kq1=Text_Content((score.get_rect().topleft[0]+560, score.get_rect().topleft[1]+353))
        kq1.color='black'
        kq1.get_text(str(data['Score']))
        kq2=Text_Content((score.get_rect().topleft[0]+560, score.get_rect().topleft[1]+400))
        kq2.color='black'
        kq2.get_text(str(data['Bonus']))
        kq3=Text_Content((score.get_rect().topleft[0]+560, score.get_rect().topleft[1]+450))
        kq3.color='black'
        kq3.get_text(str(data['Total score']))

        while(not confirm):
            for event in pg.event.get():
                if event.type==KEYDOWN:
                    confirm=True

            group_result.draw(self.screen)
            pg.display.update()

def SaveGame(result):
    today = str(date.today())

    if result==True:
            kq='WIN'
    else:
        kq='LOSE'
    global data
    data = {'Result':kq,
        'Score': SCORE,
        'Bonus': int(60-COUNTER),
        'Total score':SCORE+int(60-COUNTER),
        'Play Time': COUNTER,
        'Date': today }
    fileac.Save(data)
    infor=[ID, str(data['Score']), str(data['Date'])]
    Request_Server('SAVE', infor)

def Reset():
    global SCREENRECT, all, clock, SCORE, COUNTER, GOAL, RESULT, ID
    SCREENRECT = pg.Rect(0, 0, 1000, 700)
    all = pg.sprite.RenderUpdates()
    clock = pg.time.Clock()
    SCORE=0
    COUNTER=0
    GOAL=200
    RESULT=False
    

def main(playID='0'):
    Reset()
    global ID
    ID=playID
    hunt=Treasure_Hunt()
    SaveGame(RESULT)
  
#main()
