import pygame
import sys
import time


# Grid settings
ROWS = 6
COLS = 7
BUTTON_SIZE = 80
MARGIN = 5


GAME_OVER =  999999999
MIN_VALUE = -9999999999
MAX_VALUE =  9999999999

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def draw(board):
    WINDOW.fill(YELLOW)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE 
            if board[row][col] == 1:
                color = BLUE
            elif board[row][col] == 2: 
                color = RED
            x = MARGIN + col * (BUTTON_SIZE + MARGIN)
            y = MARGIN + row * (BUTTON_SIZE + MARGIN)
            rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)
            pygame.draw.rect(WINDOW, color, rect)
            
    pygame.display.update()
            
def button_detection(current_height):
    # Event handling
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -2

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for col in range(0, COLS):
                    row = current_height[col]
                    
                    x1 = MARGIN + col * (BUTTON_SIZE + MARGIN)
                    y2 = MARGIN + row * (BUTTON_SIZE + MARGIN)
                    x2 = MARGIN + (col + 1) * (BUTTON_SIZE + MARGIN)
                    y1 = MARGIN + (row - 1) * (BUTTON_SIZE + MARGIN)
                    
                    if mx > x1 and mx < x2 and my > y1 and my < y2:
                        return col
 


def play_move(current_height, board, index, player):
    current_height[index] -= 1
    if current_height[index] >= 0:
        board[current_height[index]][index] = player
        return True 
    
    return False

def evaluate_player(board, player):
    evaluate_counter = 0
    other_player = 0
    
    if player == 1:
        other_player = 2
    else: 
        other_player = 1
    
    #Horizontal search
    for i in range(0, ROWS):
        for j in range(0, COLS - 3):
            element_string = str(board[i][j]) + str(board[i][j+ 1])  + str(board[i][j+ 2]) + str(board[i][j+ 3])
            count_opponent = element_string.count(str(other_player))
            count_yours = element_string.count(str(player))
            
            if count_opponent != 0:
                continue
            if count_yours == 4:
                return GAME_OVER
            
            if count_yours == 3:
                evaluate_counter += 100
            elif count_yours == 2:
                evaluate_counter += 10
            elif count_yours == 1:
                evaluate_counter += 1
            
    #Vertical search
    for i in range(0, ROWS - 3):
        for j in range(0, COLS):
            element_string = str(board[i][j]) + str(board[i + 1][j])  + str(board[i + 2][j]) + str(board[i + 3][j])
            count_opponent = element_string.count(str(other_player))
            count_yours = element_string.count(str(player))
            
            if count_opponent != 0:
                continue
            if count_yours == 4:
                return GAME_OVER
            
            if count_yours == 3:
                evaluate_counter += 100
            elif count_yours == 2:
                evaluate_counter += 10
            elif count_yours == 1:
                evaluate_counter += 1
                
    #Diagonal left search
    for i in range(0, ROWS - 3):
        for j in range(0, COLS - 3):
            element_string = str(board[i][j]) + str(board[i + 1][j + 1])  + str(board[i + 2][j + 2]) + str(board[i + 3][j + 3])
            count_opponent = element_string.count(str(other_player))
            count_yours = element_string.count(str(player))
            
            if count_opponent != 0:
                continue
            if count_yours == 4:
                return GAME_OVER
            
            if count_yours == 3:
                evaluate_counter += 100
            elif count_yours == 2:
                evaluate_counter += 10
            elif count_yours == 1:
                evaluate_counter += 1
                
                
     #Diagonal left search
    for i in range(ROWS - 1, 2, -1):
         for j in range(0, COLS - 3):
            element_string = str(board[i][j]) + str(board[i - 1][j + 1])  + str(board[i - 2][j + 2]) + str(board[i - 3][j + 3])
            count_opponent = element_string.count(str(other_player))
            count_yours = element_string.count(str(player))
            
            if count_opponent != 0:
                continue
            if count_yours == 4:
                return GAME_OVER
            
            if count_yours == 3:
                evaluate_counter += 100
            elif count_yours == 2:
                evaluate_counter += 10
            elif count_yours == 1:
                evaluate_counter += 1
        
                
    return evaluate_counter



def evaluate_players(board):
    first_player_max = evaluate_player(board, 1)
    second_player_max = evaluate_player(board, 2)
    
    if first_player_max == GAME_OVER:
        return GAME_OVER
    elif second_player_max == GAME_OVER:
        return -GAME_OVER
    else:
        return first_player_max - second_player_max

def min_max(current_height, board,  alpha, beta, depth, player):
    current_evaluation = evaluate_players(board)
    
    if depth == 0 or abs(current_evaluation) == GAME_OVER:
        return current_evaluation, 0
    
    if player == 1:
        max_value = MIN_VALUE
        saved_index = -1
        for i in range(0, COLS):
            board_copy = [row[:] for row in board]
            current_height_copy = current_height[:]
            
            play_move(current_height_copy, board_copy, i, player)
            if current_height[i] == 0:
                continue
            
            curr_value, _ = min_max(current_height_copy, board_copy, alpha, beta, depth - 1, 2)
            alpha = max(alpha, curr_value)
            
            if curr_value > max_value:
                max_value = curr_value
                saved_index = i
            
            if beta <= alpha:
                break
        
        return max_value, saved_index
    
    else:
        min_value = MAX_VALUE
        for i in range(0, COLS):
            board_copy = [row[:] for row in board]
            current_height_copy = current_height[:]
            play_move(current_height_copy, board_copy, i, player)
            
            if current_height[i] == 0:
                continue
            
            curr_value, _ = min_max(current_height_copy,board_copy, alpha, beta,  depth - 1, 1)
            beta = min(beta, curr_value)
                
            if curr_value < min_value:
                min_value = curr_value
            
            if beta <= alpha:
                break
                
        return min_value, 0
            

def play(goes_first):
    plays_counted = 0
    current_height = [ROWS] * COLS
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
        ]
    
    draw(board)
    
    while True:
        
        if goes_first:
            _, correct_move = min_max(current_height, board, -999999999, 999999999,  7, 1)
            play_move(current_height, board, correct_move, 1)
        
            retVal = evaluate_players(board)
        
            plays_counted += 1
        
            draw(board)
        
            if retVal == GAME_OVER:
                print("Player 1 won")
                break
        
        goes_first = True        
        
        index = button_detection(current_height)
       
        if index == -2:
            break
       
        play_move(current_height, board, index, 2)
        
        draw(board)
        
        plays_counted += 1
        
        retVal = evaluate_players(board)
        
       
        if retVal == -GAME_OVER:
           print("Player 2 won")
           break
       
        if plays_counted == 42:
            break
    
    
    time.sleep(3)
    pygame.quit()
    sys.exit()




goes_first = True         

input_string = input("Do you want to go first?\n").upper()

if input_string == "YES":
    goes_first = False

# Initialize pygame
pygame.init()


# Window size
WIDTH = COLS * (BUTTON_SIZE + MARGIN) + MARGIN
HEIGHT = ROWS * (BUTTON_SIZE + MARGIN) + MARGIN

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("7x6 Button Grid")


play(goes_first)




