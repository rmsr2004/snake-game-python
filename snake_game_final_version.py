# Rodrigo Miguel Santos Rodrigues , 2022233032 , TP7

import time
import random
import functools
import turtle
import math

MAX_X = 600
MAX_Y = 800
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'

def load_high_score(state):
    # se já existir um high score devem guardar o valor em state['high_score']
    # Se o ficheiro já existir, o jogo lê o ficheiro
    try:
        all_of_last_high_scores = [] # Lista para guardar os highscores do ficheiro
        state['high_score'] = 0 # valor de referência
        read_high_scores = open(HIGH_SCORES_FILE_PATH, 'r') # Abrir o ficheiro
        # ler as linhas do ficheiro e guardar o highscore na lista em valor inteiro
        for line in read_high_scores: 
            first_item_of_line = int(line.split(',')[0]) 
            all_of_last_high_scores.append(first_item_of_line)
        read_high_scores.close()
        #obter o highscore mais alto da lista
        for i in range(len(all_of_last_high_scores)):
            if all_of_last_high_scores[i] > state['high_score']:
                state['high_score'] = all_of_last_high_scores[i]
    # se o ficheiro não existir, o jogo cria um
    except FileNotFoundError:
        create_high_score_file = open(HIGH_SCORES_FILE_PATH, 'w')
        create_high_score_file.close()
    pass

def write_high_score_to_file(state):
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    print("You have set a new high score! Congratulations! ---- %d"%(state['high_score']))
    username = input("User name: ")
    write_new_high_score = open(HIGH_SCORES_FILE_PATH, 'a')
    write_new_high_score.write("%d,%s\n" %(state['high_score'], username))
    write_new_high_score.close()
    pass

def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.2)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)
    #LER HIGH SCORE DO FICHEIRO
    #GUARDAR NO FICHEIRO

def update_score_board(state):
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Helvetica", 24, "normal"))

def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'

def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'

def init_state():
    state = {}
    # Informação necessária para a criação do score board
    state['score_board'] = None
    state['new_high_score'] = False
    state['high_score'] = 0
    state['score'] = 0
    # Para gerar a comida deverá criar um nova tartaruga e colocar a mesma numa posição aleatória do campo
    state['food'] = None
    state['window'] = None
    snake = {
        'head': None,                  # Variável que corresponde à cabeça da cobra
        'tail': None,                  # Variável que corresponde à cauda da cobra
        'tail_pieces' : [],            # Lista para guardar informação sobre as várias turtles da cauda da cobra
        'current_direction': None, # Indicação da direcção atual do movimento da cobra
        'speed' : 0.2,                  # Controla a velocidade da cobra. Quanto menor o valor, mais rápido é o movimento da cobra.
    }
    state['snake'] = snake
    return state

def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')
    create_score_board(state)
    create_food(state)

def move(state):
    ''' 
        Função responsável pelo movimento da cobra no ambiente.
    '''
    snake = state['snake']
    
    if snake['current_direction'] == 'up':
        y_snake = snake['head'].ycor() # guardar Y da cabeça da cobra
        snake['head'].sety(y_snake + DEFAULT_SIZE) 
    if snake['current_direction'] == 'down':
        y_snake = snake['head'].ycor()
        snake['head'].sety(y_snake - DEFAULT_SIZE)
    if snake['current_direction'] == 'left':
        x_snake = snake['head'].xcor() # guardar X da cabeça da cobra
        snake['head'].setx(x_snake - DEFAULT_SIZE)
    if snake['current_direction'] == 'right':
        x_snake = snake['head'].xcor()
        snake['head'].setx(x_snake + DEFAULT_SIZE)   
    tail_move(state)
        
def tail_move(state):
    ''' 
        Função responsável pelo movimento da cauda da cobra.
    '''    
    snake = state['snake']
    pieces = state['snake']['tail_pieces']
    '''
        Movimentar as partes da cauda em relação à primeira parte da cauda
    '''
    for i in range(len(pieces)-1,0,-1): # percorrer a lista do maior para o mais pequeno
        x_tail = pieces[i-1].xcor() 
        y_tail = pieces[i-1].ycor()
        # as caudas vão para a posição da que está á sua frente
        pieces[i].goto(x_tail, y_tail)
    '''
        Primeira parte da cauda.
    '''
    if len(pieces) > 0:
        x_tail = state['snake']['head'].xcor()
        y_tail = state['snake']['head'].ycor()
        if snake['current_direction'] == 'up':
            pieces[0].goto(x_tail, y_tail -DEFAULT_SIZE)
        if snake['current_direction'] == 'down':
            pieces[0].goto(x_tail,y_tail + DEFAULT_SIZE)
        if snake['current_direction'] == 'left':
            pieces[0].goto(x_tail + DEFAULT_SIZE,y_tail)
        if snake['current_direction'] == 'right':
            pieces[0].goto(x_tail - DEFAULT_SIZE, y_tail) 
    
def tail_growth(state):
    '''
        Função responsável pelo crescimento da cauda da cobra.
    '''
    tail = state['snake']['tail']
    
    tail = turtle.Turtle()
    tail.shape(SNAKE_SHAPE)
    tail.color('black') 
    tail.pu()
    state['snake']['tail_pieces'].append(tail) # guardar os pedaços da cauda na lista 'tail_pieces'
    
def create_food(state):
    ''' 
        Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias, mas dentro dos limites do ambiente.
    '''
    # a informação sobre a comida deve ser guardada em state['food']
    state['food'] = turtle.Turtle()
    state['food'].showturtle()
    state['food'].shape('circle')
    state['food'].penup()    
    #GERAR POSIÇÃO ALEATÓRIA
    random_food_x = random.randint(-MAX_X/2 + 40,MAX_X/2 - 40)
    random_food_y = random.randint(-MAX_Y/2 + 40,MAX_Y/2 - 40)
    # se a comida for gerada na mesma posição que a cabeça
    if ((random_food_x == state['snake']['head'].xcor()) and (random_food_y ==  state['snake']['head'].ycor())):
        state['food'].hideturtle()
        random_food_x = random.randint(-MAX_X/2 + 40,MAX_X/2 - 40)
        random_food_y = random.randint(-MAX_Y/2 + 40,MAX_Y/2 - 40)
    # se a comida for gerada na mesma posição que a cauda 
    for piece in state['snake']['tail_pieces']:
        if ((random_food_x == piece.xcor()) and (random_food_y == piece.ycor())):
            state['food'].hideturtle()
            random_food_x = random.randint(-MAX_X/2 + 40,MAX_X/2 - 40)
            random_food_y = random.randint(-MAX_Y/2 + 40,MAX_Y/2 - 40)
            state['food'].showturlte()
    state['food'].goto(random_food_x, random_food_y) 
            
def check_if_food_to_eat(state):
    ''' 
        Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida estiver a uma distância inferior a 15 pixels a cobra pode comer a peça de comida. 
    '''
    #para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do state: state['high_score'], state['score'] e state['new_high_score']
    food = state['food']
    snake = state['snake']
    
    distance = math.sqrt((snake['head'].xcor() - food.xcor() )**2 + (snake['head'].ycor() - food.ycor() )**2) #Distância entre a cabeça da cobra e a comida
    if distance < 15:
        food.hideturtle() 
        tail_growth(state)
        create_food(state)
        snake['speed'] = snake['speed'] - 0.005 # acelerar a velocidade à medida que o score aumenta
        if snake['speed'] < 0: # não pode haver velocidades negativas
            snake['speed'] = 0
        state['score'] = state['score'] + 10 # aumento do score
        #Se o score atual for maior que o recorde
        if state['score']  > state['high_score']:
            state['high_score'] = state['score']
            state['new_high_score'] = True        
        update_score_board(state)

def boundaries_collision(state):
    ''' 
        Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a função deverá returnar o valor booleano True, caso contrário retorna False.
    '''
    snake = state['snake']
    
    if snake['head'].xcor() >= MAX_X/2 or snake['head'].xcor() <= -MAX_X/2 or snake['head'].ycor() >= MAX_Y/2 or snake['head'].ycor() <= -MAX_Y/2:   
        state['window'].exitonclick()
        return True
    else:
        return False

def check_collisions(state):
    '''
        Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com os limites do ambiente. No entanto deverá escrever o código para verificar quando é que a tartaruga choca com uma parede ou com o seu corpo.
    '''
    snake = state['snake']
    pieces = snake['tail_pieces']
   
    for piece in pieces:
        distance = math.sqrt((snake['head'].xcor() - piece.xcor() )**2 + (snake['head'].ycor() - piece.ycor() )**2) #Distância entre a cabeça e as turtles que compõem a cauda
        if distance < 15:
            state['window'].exitonclick()
            return True
    return boundaries_collision(state)

def main():
    state = init_state()
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        move(state)
        time.sleep(state['snake']['speed'])
    print("YOU LOSE!")
    if state['new_high_score']:
        write_high_score_to_file(state)
main()