import pandas as pd
import os
from csv import DictWriter, writer
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sympy import rotations

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(main_dir, '..'))

file = os.path.join(main_dir, "data", 'Result.csv')
field_names=['Result', 'Score', 'Bonus', 'Total score', 'Play Time', 'Date']
save_path=lambda filename: os.path.join(main_dir, "data_solve", filename)
plt.rcParams.update({'axes.facecolor':'lightblue', 'font.size': 15})
plt.rcParams.update({'text.color': "red", 'axes.labelcolor': "green"})

  
def Save(data):

    with open(file, 'a') as f_object:
      
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
  
        dictwriter_object.writerow(data)
  
        f_object.close()

class Graph():

    def __init__(self):
        self.data = pd.read_csv(file)
        self.data['ID'] = self.data.index
    
    def Type1(self):
        '''Score statistics'''
        cartier=self.data.drop(['Result', 'Play Time', 'Date'] , axis = 1 , inplace=False)
        cartier.to_csv(save_path('ScoreStatis.csv'))

        if len(cartier.index>6):
            cartier=cartier.tail(6)

        cartier.plot(x="ID", y=['Score', 'Bonus', 'Total score'], kind="bar")
        plt.title('Score Statistics')
        plt.xlabel('Play Turn')
        plt.ylabel('Score')
        plt.legend(loc= "upper left")
        plt.savefig(save_path('ScoreStatis.png'))
       
        return 'ScoreStatis.png', 'ScoreStatis.csv'
        
    def Type2(self):
        '''Play time statistic'''
        cartier=self.data.drop(['Result', 'Score', 'Bonus', 'Total score','Date'] , axis = 1 , inplace=False)
        cartier.to_csv(save_path('TimeStatis.csv'))

        if len(cartier.index>10):
            cartier=cartier.tail(10)
            
        x=cartier['ID']
        y=cartier['Play Time']
        plt.plot(x, y)
        plt.ylabel('Time(s)')
        plt.xlabel('Play Turn')
        # plt.xticks(np.arange(0,len(x) , 1))
        plt.title('Time Statistics')
        plt.savefig(save_path('TimeStatis.png'))
        return 'TimeStatis.png', 'TimeStatis.csv'

    def Type3(self):
        '''Count play turn by date'''

        cartier = self.data.groupby(['Date'])['ID'].count().to_frame()
        cartier.columns=['No_play']
        sort=cartier.sort_values(by=['No_play'], ascending=False, inplace=False)
        sort.reset_index(level = [0], inplace=True)
        sort.to_csv(save_path('TurnbyDateStatis.csv'))

        if len(sort.index>10):
            sort=sort.tail(10)

        sort.plot(x="Date", y=['No_play'], kind="bar")
        plt.title('Number of Play Time by Date Statistics')
        plt.xlabel('Date')
        plt.xticks(rotation=15)
        plt.ylabel('No_playtime')
        plt.savefig(save_path('TurnbyDateStatis.png'))
        
        return 'TurnbyDateStatis.png', 'TurnbyDateStatis.csv'

    def Type4(self):

        '''Win-Lose Rate'''

        color=('pink', 'green')

        cartier = self.data.groupby(['Result'])['ID'].count().to_frame()
        cartier.columns=['Time']
        cartier.reset_index(level = [0], inplace=True)
        cartier['Rate']=cartier['Time']/len(self.data.index)
        cartier['Rate']=cartier['Rate'].round(2)
        def func(pct, allvalues):
            absolute = int(pct / 100.*np.sum(allvalues))
            return "{:.1f}%\n({:d} times)".format(pct, absolute)
        
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(cartier['Rate'],
                                        autopct = lambda pct: func(pct, cartier['Time']),
                                        labels = cartier['Result'],
                                        colors = color,
                                        startangle = 90,
                                        textprops = dict(color ="black"))
        
        plt.setp(autotexts, size = 15)
        ax.set_title("Result Rate")
        plt.savefig(save_path('ResultRate.png'))
        cartier.to_csv(save_path('ResultRate.csv'))
        return 'ResultRate.png', 'ResultRate.csv'

    def get_highest_score(self):
        col=self.data['Total score']
        max_value=col.max()
        return max_value


    def get_option(self, ReqID):
        if ReqID==1:
            return type1
        elif ReqID==2:
            return type2
        elif ReqID==3:
            return type3
        else:
            return type4
        
def run_analyse():
    global graph, type1, type2, type3, type4
    graph=Graph()
    type2=graph.Type2()
    type1=graph.Type1()
    type3=graph.Type3()
    type4=graph.Type4()

    
        


