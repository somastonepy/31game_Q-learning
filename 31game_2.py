import random
import matplotlib.pyplot as plt
import numpy as np

# グローバル変数
num_games=10000
gamenum=31
ALPHA = 0.01     # 学習係数
GAMMA = 0.80   # 割引率
EPSILON = 0.2   # 行動選択のランダム性を決定

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

    def make_move(self,now_num):
        print('now_num = ',now_num  )
        next_num=int(input('  please select number 1 or 2 or 3 : '))+now_num
        return next_num

class Qlearn(Agent):
    def __init__(self,name):
        super().__init__(name)
        self.qvalue = [0 for i in range(gamenum+8)]
        for i in range(gamenum):
            self.qvalue[i] = np.random.randint(0,101) 
    

    def make_move(self,now_num):
        next_num=selecta(now_num,self.qvalue)
        self.qvalue[next_num]=updateq(next_num,self.qvalue)
            
        return next_num
    
class Qlearn_plus(Agent):
    def __init__(self,name):
        super().__init__(name)
        self.qvalue = [0 for i in range(gamenum+8)]
        self.log=[]
        for i in range(gamenum):
            self.qvalue[i] = np.random.randint(0,101) 
    

    def make_move(self,now_num):
        self.log.append(now_num)
        next_num=selecta(now_num,self.qvalue)
        self.qvalue[next_num]=updateq(next_num,self.qvalue)
        if next_num == gamenum:
            # print(self.log)
            for xx in self.log:
                self.qvalue[xx]=updateq(xx,self.qvalue)
        return next_num
    
class Strong(Agent):
    def make_move(self,now_num):
        for i in range(3):
            now_num+=1
            if (now_num+gamenum-1)%4 == 0:
                return now_num
        return now_num
    
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
        # print(s+6,len(qvalue))
        q_1=qvalue[s+2]+qvalue[s+3]+qvalue[s+4]
        q_2=qvalue[s+3]+qvalue[s+4]+qvalue[s+5]
        q_3=qvalue[s+4]+qvalue[s+5]+qvalue[s+6]
        #Ｑ値最大値を選択
        if (q_1) > (q_2):
            if (q_2) > (q_3):
                s+=3
            else:
                s+=2
        else:
            if (q_1) > (q_3):
                s+=3
            else:
                s+=1
    if s>gamenum:
        s=gamenum  
    return  s
        

def updateq(s,qvalue):
    """Q値を更新する"""
    
    # 勝ち確定
    if s==gamenum-1:
        # 報酬の付与
        qv = qvalue[s] + int(ALPHA * (2000 - qvalue[s]))
        return qv
        # 報酬を与えるノードを増やす
        # 他のノードを追加する場合は
        # 下記2行のコメントを外す
#        elif s == 11:
#            qv = qvalue[s] + int(ALPHA * (500 - qvalue[s]))

    #負け確定
    elif s > gamenum-5 and s != gamenum-1:
        qv = qvalue[s] + int(ALPHA * (-100 - qvalue[s]))
        return qv
    

    # 上記以外
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
            winner=player2
            break
        now_num = player2.make_move(now_num)
        # print(player2.name + str(now_num))
        if now_num>gamenum-1:
            winner=player1
            break
    # Tit-for-tat戦略の場合、相手の行動を記憶
    
    if isinstance(agent1, Qlearn_plus):
        print(agent1.qvalue)
        # agent1.log = []
    if isinstance(agent2, Qlearn_plus):
        # print(agent2.qvalue)
        agent2.log = []
    return winner

def play_multiple_games(agent1, agent2, num_games):
    cnt_1=0
    cnt_2=0
    
    for i in range(num_games):
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
you=Qlearn_plus("you1")
me=TitForTat("rand_plus")

play_multiple_games(me, you, num_games)
me=All1("All1")
play_multiple_games(me, you, num_games)
me=All2("All2")
play_multiple_games(me, you, num_games)
me=All3("All3")
play_multiple_games(me, you, num_games)
me=RandomAgent("rand")
play_multiple_games(me, you, num_games)
me=Strong("st")
play_multiple_games(me, you, num_games)


me=TitForTat("rand_plus")
play_multiple_games(me, you, num_games)
you2=Qlearn("you2")
play_multiple_games(you2, you, num_games)
me=Alternator("me")
winner=play_game(me,you)
print('winner = ',winner.name)
for i in range(gamenum+2):
    if(i+4-(gamenum-1)%4)%4 == 0:
        print()
    print(i,you.qvalue[i],'--',you2.qvalue[i])
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