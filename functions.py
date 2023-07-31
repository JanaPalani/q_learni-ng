import pygame 
import time
import random
from math import exp
pygame.init() 
width, height = 250,250
box_dim = 50
plot = pygame.display.set_mode((width, height))


grid_val  = {}
state_action = {}
pit_val,reward_val = {(3,1):-4,(3,3):-2,(1,2):-5},{(4,4):10,(0,4):1}
man_pos_x ,man_pos_y= (2,2)
learning_rate = 0.01
discount = 0.95
reward = 0
actions = {'up':0,'down':1,'left':2,'right':3}
movements = {'left':(-1,0) , 'right':(1,0) , 'up':(0,-1) , 'down':(0,1) }
direction_finding = {0:'up',1:'down',2:'left',3:'right'}






def explore():
    global man_pos_x , man_pos_y ,positions_episode

    while True:
        start = (man_pos_x,man_pos_y)
        option = random.choice(seq=['up','down','left','right'])
        man_pos_x += movements[option][0]
        man_pos_y += movements[option][1]
        end = (man_pos_x,man_pos_y)
        if man_pos_x in range(0,5) and man_pos_y in range(0,5):
            break 
        else:
            man_pos_x = start[0]
            man_pos_y = start[1]   
    
    return (start,option,end)


def exploit():
    global man_pos_x,man_pos_y,positions_episode
    start =  (man_pos_x,man_pos_y)
    possible_directions = []
    if man_pos_x <= 3 :
        possible_directions.append(['right',3])
    if man_pos_x >= 1 :
        possible_directions.append(['left',2])
    if man_pos_y <= 3 :
        possible_directions.append(['down',1])
    if man_pos_y >= 1 :
        possible_directions.append(['up',0])
    max_val = -99999999999999999999999999999999
    direction = None
    for each in possible_directions:
        val = state_action[start][each[1]]
        if val > max_val:
            max_val = val
            direction = each[0]


    man_pos_x += movements[direction][0]
    man_pos_y += movements[direction][1]

    end = (man_pos_x,man_pos_y)
    return (start,direction,end)

        
        
        


def update_val(start,action,next):
    global state_action , reward
    reward = grid_val[next]
    action = actions[action]
    present_val = (1-learning_rate)*state_action[start][action]
    new_learn = learning_rate*(reward*2 + discount * max(state_action[next]))
    state_action[start][action] = present_val + new_learn
    return 

def grid_and_rewards():
    for row_num in range(int(width/box_dim)):
        for column_num in range(int(height/box_dim)):
            grid_val[(row_num,column_num)] = 0
            state_action[(row_num,column_num)] = [0,0,0,0]

    for key,value in pit_val.items():
        grid_val[key] = value
    
    for key,value in reward_val.items():
        grid_val[key] = value
    
    return grid_val
   


grid_and_rewards()

moves_per_episode = 1000
epsilon_value = 0.9
start_exploring = False

clock = pygame.time.Clock()


current_episode = 1
run = True 
frames  = 10                                
while run :
    clock.tick(frames)
    positions_episode = []
    plot.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start , _ , end = exploit()
                print(end)
                if end == (4,4):
                    
                    run = False

                
            if event.key == pygame.K_s:
                start_exploring =True
            
            if event.key == pygame.K_q:
                start_exploring = False 
            
            if event.key == pygame.K_DOWN:
                frames = 10
                print('frames reduced ')
            if event.key == pygame.K_UP:
                frames = 100
                print('frames incresed ')

        
    for key , value in grid_val.items():
        x , y = key
        pygame.draw.rect(plot,(150,150,0),(x*box_dim,y*box_dim,box_dim,box_dim),1)
        if value in range(1,11):
            pygame.draw.rect(plot,(0,value*25,0),(x*box_dim,y*box_dim,box_dim,box_dim))
        elif value in range(-5,0):
            pygame.draw.rect(plot,((-value)*50,0,0),(x*box_dim,y*box_dim,box_dim,box_dim))
    


    if start_exploring:
        number_rand = random.uniform(0,1)
        if number_rand <= epsilon_value:
            start , action , end = explore()

        else:
            start , action , end = exploit()
        update_val(start,action,end)
        current_episode += 1


    

    pygame.draw.rect(plot,(0,150,150),(man_pos_x*box_dim,man_pos_y*box_dim,box_dim,box_dim))
    pygame.display.flip()

    if current_episode == moves_per_episode:
        start_exploring = False
        man_pos_x,man_pos_y = (0,0)
        frames = 10
        current_episode += 1
    

            
