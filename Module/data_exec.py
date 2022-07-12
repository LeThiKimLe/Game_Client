
from matplotlib.pyplot import get
import pandas as pd
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(main_dir, '..'))

load_file=lambda filename:os.path.join(main_dir, 'Gamedata', filename)


def get_question():
   
    df = pd.read_csv(load_file('Question.csv'))
    return df
    
def get_answer(QuesID):
    df = pd.read_csv(load_file('Answer.csv'))
    for i in range(len(df)):
        if QuesID ==str(df.iloc[i,0]).strip():
            x=df.iloc[i,1]
            return x
            

def get_multichoices(QuesID):
    df=pd.read_csv(load_file('Multichoices.csv'))
    for i in range(len(df)):
        if QuesID==str(df.iloc[i][0]).strip():

            x=df.iloc[[i]]
            return x

# print(get_question())
# print(type(get_answer('Q01')))
# print(get_multichoices('Q01'))

def load_question():

    def load_multichoices(Ques):
        df=get_multichoices(Ques)
        return list(df.iloc[0][1:].values)

    ques_table=get_question()
    pick=ques_table.sample()
    question= pick['Question'].iloc[0]
    quesID= pick['QuesID'].iloc[0]
    level= pick['QuesLevel'].iloc[0]
    choices=load_multichoices(quesID.strip())
    return quesID, [question, choices, level]

load_question()
