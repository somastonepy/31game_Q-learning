import random
import matplotlib.pyplot as plt

# 利得表を辞書で定義
payoff = {'T': 5, 'R': 3, 'P': 1, 'S': 0}

# エージェントの定義
class Agent:
    def __init__(self):
        self.payoff = 0 # 利得

    def make_move(self): # 戦略
        pass

# AllC（常に協力）
class AllC(Agent):
    def __init__(self):
        super().__init__()

    def make_move(self):
        return 'C'

# AllD（常に裏切り）
class AllD(Agent):
    def __init__(self):
        super().__init__()

    def make_move(self):
        return 'D'

# Random（ランダムに行動）
class RandomAgent(Agent):
    def __init__(self):
        super().__init__()

    def make_move(self):
        return random.choice(['C', 'D'])
        
# Tit-for-tat（しっぺ返し）
class TitForTat(Agent):
    def __init__(self):
        super().__init__()
        self.memory = 'C'

    def make_move(self):
        return self.memory

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
class USG(Agent):
    def __init__(self):
        super().__init__()
        self.memory='C'

    def make_move(self):
        if(self.payoff>2):
            return self.memory
        elif(self.memory=='C'):
            return 'D'
        else:
            return 'C'

def play_game(agent1, agent2):
    move1 = agent1.make_move()
    move2 = agent2.make_move()
    
    if move1 == 'C' and move2 == 'C':
        agent1.payoff += payoff['R']
        agent2.payoff += payoff['R']
    elif move1 == 'C' and move2 == 'D':
        agent1.payoff += payoff['S']
        agent2.payoff += payoff['T']
    elif move1 == 'D' and move2 == 'C':
        agent1.payoff += payoff['T']
        agent2.payoff += payoff['S']
    else:
        agent1.payoff += payoff['P']
        agent2.payoff += payoff['P']

    # Tit-for-tat戦略の場合、相手の行動を記憶
    if isinstance(agent1, TitForTat):
        agent1.memory = move2
    if isinstance(agent2, TitForTat):
        agent2.memory = move1

def play_multiple_games(agent1, agent2, num_games=10):
    payoffs1 = []
    payoffs2 = []
    for _ in range(num_games):
        agent1.payoff = 0
        agent2.payoff = 0
        
        play_game(agent1, agent2)
        payoffs1.append(agent1.payoff)
        payoffs2.append(agent2.payoff)
    return payoffs1, payoffs2

# エージェントの作成
cooperator = AllC()
defector = AllD()
random_agent1 = RandomAgent()
random_agent2 = RandomAgent()
tit_for_tat1 = TitForTat()
tit_for_tat2 = TitForTat()
alternator=Alternator()
unison=USG()
# それぞれの組み合わせでゲームをプレイ
payoffs_allc_tit_for_tat, payoffs_tit_for_tat_allc = play_multiple_games(unison, tit_for_tat1)
# 箱ひげ図をプロット
data = [payoffs_allc_tit_for_tat, payoffs_tit_for_tat_allc]
# print(data)

plt.figure(figsize=(10, 6))
X=0
Y=0
x=[]
y=[]
for i in range(10):
    X+=data[0][i]
    Y+=data[1][i]
    x.append(X)
    y.append(Y)

print(x)
# print(y)
plt.plot(y,marker='o',label='TFT')
plt.plot(x,marker='o',label='USG')
plt.legend()
plt.grid()
plt.xlabel('Game Number')
plt.ylabel('Alternator Payoff')
plt.title('Payoff of TFT vs USG')
plt.show()