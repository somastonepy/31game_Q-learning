import random
import matplotlib.pyplot as plt
import numpy as np

# グローバル変数
num_games=1000
gamenum=31
ALPHA = 0.01     # 学習係数
GAMMA = 0.6    # 割引率
EPSILON = 0.3   # 行動選択のランダム性を決定

# 利得表を辞書で定義
payoff = {'T': 5, 'R': 3, 'P': 1, 'S': 0}

# エージェントの定義
class Agent:
    def __init__(self,name):
        self.name=name

    def make_move(self): # 戦略
        pass

# All1（常に協力）
class All1(Agent):

    def make_move(self,now_num):
        return now_num+1

# All2（常に裏切り）
class All2(Agent):

    def make_move(self,now_num):
        return now_num+2

# All3（常に裏切り）
class All3(Agent):

    def make_move(self,now_num):
        return now_num+3
    

# Random（ランダムに行動）
class RandomAgent(Agent):

    def make_move(self,now_num):
        return now_num+random.randint(1,3)
        
# Tit-for-tat（しっぺ返し）
class TitForTat(Agent):
    def make_move(self,now_num):
        if now_num>26 and now_num<30:
            return 30
        return now_num+random.randint(1,3)
#Alternator
class Alternator(Agent):
    def __init__(self):
        super().__init__()
        self.cnt=0

    def make_move(self):
        self.cnt+=1
        if(self.cnt%2 == 0):
            return 'C'
        else:
            return 'D'

#最初はC 前回0点または１点なら戦略を変える。
class Qlearn(Agent):
    def __init__(self,name):
        super().__init__(name)
        self.qvalue = [0 for i in range(gamenum+3)]
        for i in range(gamenum):
            self.qvalue[i] = np.random.randint(0,101) 
        self.log_win=[]
        self.log_lose=[]

    def make_move(self,now_num):
        self.log_lose.append(now_num)
        next_num=selecta(now_num,self.qvalue)
        self.log_win.append(next_num)
        if next_num==gamenum:
            for i in self.log_lose:
                #print(i)
                self.qvalue[i]=updateq(i,self.qvalue)
            #print(self.qvalue)
        elif next_num==gamenum-1:

            for i in self.log_win:
                self.qvalue[i]=updateq(i,self.qvalue)
            #print(self.qvalue)
        return next_num
    
def selecta(s,qvalue):
    """行動を選択する"""
    if s==gamenum-1:
        s = gamenum
    # ε-greedy法による行動選択:
    elif np.random.random()<EPSILON:
        # ランダムに行動
        zz=np.random.randint(0,3)
        if zz == 0:
            s+=1
        elif zz == 1:
            s+=2
        else:
            s+=3
  
    else: 
        #Ｑ値最大値を選択
        if (qvalue[s+1]) > (qvalue[s+2]):
            if (qvalue[s+1]) > (qvalue[s+3]):
                s+=1
            else:
                s+=3
        else:
            if (qvalue[s+2]) > (qvalue[s+3]):
                s+=2
            else:
                s+=3
    if s>gamenum:
        s=gamenum  
    return  s
        

def updateq(s,qvalue):
    """Q値を更新する"""
    
    # 最下段の場合
    if s == gamenum-1:
        # 報酬の付与
        qv = qvalue[s] + int(ALPHA * (1000 - qvalue[s]))
        return qv
        # 報酬を与えるノードを増やす
        # 他のノードを追加する場合は
        # 下記2行のコメントを外す
#        elif s == 11:
#            qv = qvalue[s] + int(ALPHA * (500 - qvalue[s]))
    
    # 最下段以外
    elif (qvalue[s+1]) > (qvalue[s+2]):
        if (qvalue[s+1]) > (qvalue[s+3]):
            qmax = qvalue[s+1]
        else:
            qmax = qvalue[s+3]
    else:
        if (qvalue[s+2]) > (qvalue[s+3]):
            qmax = qvalue[s+2]
        else:
            qmax = qvalue[s+3]
    # Q値を更新
    qv = qvalue[s] + int(ALPHA * (GAMMA * qmax - qvalue[s])) 
    return  qv

def play_game(agent1, agent2):
    xx=random.randint(0,1)
    if xx==0:
        player1=agent1
        player2=agent2
    else:
        player1=agent2
        player2=agent1

    now_num=0
    while now_num < gamenum:

        now_num = player1.make_move(now_num)
        # print(player1.name + str(now_num))
        if now_num>gamenum-1:
            return player2
        now_num = player2.make_move(now_num)
        # print(player2.name + str(now_num))
        if now_num>gamenum-1:
            return player1
    

    # Tit-for-tat戦略の場合、相手の行動を記憶
    if isinstance(agent1, TitForTat):
        agent1.memory = move2
    if isinstance(agent2, TitForTat):
        agent2.memory = move1

def play_multiple_games(agent1, agent2, num_games):
    cnt_1=0
    cnt_2=0
    
    for i in range(num_games):
        agent2.log_win=[]
        agent2.log_lose=[]
        agent1.log_win=[]
        agent1.log_lose=[]
        winner=play_game(agent1, agent2)
        #print('winner : '+winner.name)
        if winner==agent1:
            cnt_1+=1
        else:
            cnt_2+=1
        for j in range(gamenum):
            Qvalue[j][i]=agent2.qvalue[j]
    print(agent1.name,str(cnt_1*100/num_games)+'%',agent2.name,str(cnt_2*100/num_games)+'%')
        

# エージェントの作成

Qvalue=[[0 for i in range(num_games)]for j in range(gamenum)]
you=Qlearn("qlearn")
me=TitForTat("rand")
play_multiple_games(me, you, num_games=1000)
# me=All1("rand")
# play_multiple_games(me, you, num_games=10000)
# me=All2("rand")
# play_multiple_games(me, you, num_games=10000)
# me=All3("rand")
# play_multiple_games(me, you, num_games=10000)
# me=RandomAgent("rand")
# play_multiple_games(me, you, num_games=10000)



me=RandomAgent("rand")
#play_multiple_games(me, you, num_games)
for i in range(gamenum):
    if(i+4-(gamenum-1)%4)%4 == 0:
        print()
    print(i,you.qvalue[i])
# それぞれの組み合わせでゲームをプレイ
# payoffs_allc_tit_for_tat, payoffs_tit_for_tat_allc = play_multiple_games(unison, tit_for_tat1)
# # 箱ひげ図をプロット
# data = [payoffs_allc_tit_for_tat, payoffs_tit_for_tat_allc]
# # print(data)

# plt.figure(figsize=(10, 6))
# X=0
# Y=0
# x=[]
# y=[]
# for i in range(10):
#     X+=data[0][i]
#     Y+=data[1][i]
#     x.append(X)
#     y.append(Y)

for j in range(gamenum):
    plt.plot(Qvalue[j],marker='o')
plt.show()
#print(x)
# print(y)
# plt.plot(y,marker='o',label='TFT')
# plt.plot(x,marker='o',label='USG')
# plt.legend()
# plt.grid()
# plt.xlabel('Game Number')
# plt.ylabel('Alternator Payoff')
# plt.title('Payoff of TFT vs USG')
# plt.show()