
from multiprocessing.connection import wait
import pygame
from pygame.locals import *
import os
from time import sleep
import pandas as pd
import Module.file_action as fileac
from csv import reader

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(main_dir, '..'))

def scale(surface,scale_in):
    x=surface.get_width()
    y=surface.get_height()
    surface = pygame.transform.scale(surface, (x*scale_in, y*scale_in))
    return surface


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pygame.image.load(file)
        surface = scale(surface, 0.8)
        pygame.Surface.set_colorkey(surface, [0,0,0])
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()

class button():
    def __init__(self, pos , text, func=None):
        
        self.images=[load_image('but1.png'), load_image('but2.png')]
        self.get_rect(self.images[1])
        self.x = pos[0]
        self.y = pos[1]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.text = text
        self.chosen=False
        self.function=func

    def get_rect(self, image):
        self.image=image
        self.image=scale(self.image, 4)

    def draw(self,win):
        #Call this method to draw the button on the screen
        
        if self.text != '':
            win.blit(self.image, (self.x, self.y))
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))
            pygame.display.update()
        
    def isOver(self, pos, screen):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.chosen=True
                self.update(screen)
                return True
        return False

    def update(self,screen):
        if self.chosen==True:
            self.get_rect(self.images[0])
        else:
            self.get_rect(self.images[1])
        self.draw(screen)


class Statistics():

    def __init__(self, graph):
        pygame.init()
        self.display = pygame.display.set_mode((1250, 800))
        self.display.fill('#9900FF')
        self.FPS_CLOCK = pygame.time.Clock()
        self.graph=graph
        self.mode='Graph'
        self.put_frame()
        self.put_button()
        self.main_loop()

    def put_frame(self):
        self.frame=load_image('framedata.png')
        self.frame=scale(self.frame, 2.5)
        pygame.Surface.set_colorkey(self.frame, [255,255,255])
        self.display.blit(self.frame, (250,50))

        self.table_btn=button((500, 20), 'Data Table')
        self.graph_btn=button((740, 20), 'Graph')
        self.table_btn.draw(self.display)
        self.graph_btn.draw(self.display)

        self.select_mode=[self.table_btn, self.graph_btn]
        pygame.display.update()

    def put_button(self):
        
        self.btn=[]
        option={1:'Score Statistics', 2:'Time Statistics', 3:'Date Statistic', 4:'Result Rate'}
        x=20
        y=100
        for i in range(4):
            op=button((x, y+i*150), option[i+1] , i+1)
            op.draw(self.display)
            self.btn.append(op)
        pygame.display.update()
        

    def main_loop(self):
        pos=(0,0)
        run=True
        while run:
            for event in pygame.event.get():
                # if event.type == QUIT:
                #     pygame.quit()
                #     sys.exit()
                
                if event.type==KEYDOWN:
                    if event.unicode == "q":
                        run=False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        pos=pygame.mouse.get_pos()
                    
                        if self.table_btn.isOver(pos,self.display):
                            self.mode='Table'
                            self.graph_btn.chosen=False
                            self.graph_btn.update(self.display)

                        elif self.graph_btn.isOver(pos, self.display):
                            self.mode='Graph'
                            self.table_btn.chosen=False
                            self.table_btn.update(self.display)

                        else:
                            for op in self.btn:
                                if op.isOver(pos, self.display):
                                    image, file = self.graph.get_option(op.function)
                                    self.show(image, file)
                                else:
                                    op.chosen=False
                                op.update(self.display)

            pygame.display.update()
            self.FPS_CLOCK.tick(30)

    def show(self, image, file):
        if self.mode=='Table':
            self.show_datatable(file)
        else:
            self.show_graph(image)

    def show_graph(self, graph_in):

        def delete_old():
            cover=pygame.Surface((590, 560))
            cover.fill('#9900FF')
            self.display.blit(cover, (450, 155))
        delete_old()
        image=load_image(fileac.save_path(graph_in))
        image=scale(image, 1.2)
        # pygame.Surface.set_colorkey(image, [255,255,255])
        self.display.blit(image, (440, 200))
        pygame.display.update()

    def show_datatable(self, data_file):

        def put_col(list_char, x, y):
            
            font = pygame.font.SysFont('comicsans', 30)
            for word in list_char:
                text = font.render(str(word), 1, (0,0,0))
                self.display.blit(text, (x, y))
                y+=75
            pygame.display.update()

        def put_table(x_pos, y_pos, begin_row=0, end_row=0):
            for i in range(len(head)):
                col=data.iloc[begin_row:end_row,i].to_list()
                col.insert(0,head[i])
                put_col(col, x_pos, y_pos)
                if str(col[0])=='Total score' or str(col[0])=='Date' or str(col[0])=='Play Time':
                    x_pos+=120
                x_pos+=110

        def delete_old():
            cover=pygame.Surface((600, 545))
            cover.fill('#9900FF')
            self.display.blit(cover, (440, 175))

        delete_old()
        file=fileac.save_path(data_file)
        data = pd.read_csv(file)
        head=data.columns.to_list()
        head[0]=''
        x_post=450
        y_post=200
        no_rows=len(data.index)
        if no_rows<=6:
            put_table(x_post, y_post, 0, no_rows)
        else:
            i=0
            start=0
            while(i in range(0, no_rows)):
                if i+6<no_rows:
                    start=i
                    end=i+6
                    next_i=i+6
                    
                else:
                    start=i
                    end=no_rows

                prev_i=start-6
                next_i=end

                put_table(x_post, y_post,start,end)
                wait=True
                while(wait):
                    for event in pygame.event.get():

                        if event.type==KEYDOWN:
                            if event.key == pygame.K_DOWN:
                                if (next_i in range(no_rows)):
                                    delete_old()
                                    x_post=450
                                    y_post=200
                                    i=next_i
                                    wait=False
                            elif event.key == pygame.K_UP:
                                if (prev_i in range(no_rows)):
                                    delete_old()
                                    x_post=450
                                    y_post=200
                                    i=prev_i
                                    wait=False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_presses = pygame.mouse.get_pressed()
                            if mouse_presses[0]:
                                return True

def run_statis():
    graph=fileac.Graph()
    fileac.run_analyse()
    data_view=Statistics(graph)
