import pygame
import sys
from scrape import getGame
from math import floor, ceil
import tkinter as tk
from tkinter import *
import buzzer
from time import time, sleep
m = 1 #size modifier
width, height = 900*m, 540*m+50


root = tk.Tk()
embed = tk.Frame(root, width=width, height=height) #creates embed frame for pygame window
#embed.grid(columnspan = (600), rowspan = 500) # Adds grid
#embed.pack(side = LEFT) #packs window to the left

players = []
scores = {player:0 for player in players}

timer = 0

Game_ID = 1

display = 1 # 1-board 2-question 3-answer 4-daily double

buzzedPlayer = None

def resetBuzzers():
    global buzzedPlayer,timer
    buzzer.reset()
    buzzedPlayer = None
    timer = 0

def changeGame():
    global rounds, roundMask, currentRound
    rounds = getGame(int(input_game_id.get()))
    currentRound = 1
    roundMask = [[True for x in range(5)] for y in range(6)]


def update_score(player, amount, correct = False, question = False):
    global display, timer
    scores[players[player]] += amount

    if question and display == 2:
        if correct:
            money = (ques[1]+1)*200*currentRound
            resetBuzzers()
            display += 1
        else:
            money = -(ques[1]+1)*200*currentRound
            resetBuzzers()
            timer = time()
        
        scores[players[player]] += money
    elif question and display == 3:
        display = 1
        roundMask[ques[0]][ques[1]] = False
        displayAnswer()
    label_var[player].set(f"{players[player]}: {scores[players[player]]}")


def startTimer():
    global timer
    resetBuzzers()
    timer = time()

game_code = buzzer.startSession() # starts buzzer

code_label = tk.Label(root, text=game_code)
code_label.grid(row=1, column = 0, pady=5)

start_timer = tk.Button(root, text="Start Timer", command=startTimer,bg="white",fg="black")
start_timer.grid(row=2, column=0, pady=5, padx=5)

answer_label = tk.Label(root, text="")
answer_label.grid(row=3, column=0,pady=5)

def getPlayers():
    currentPlayers = buzzer.getPlayerNames()
    for player in currentPlayers:
        if player not in scores:
            scores[player] = 0
            players.append(player)
    get_players.grid(row = 0, column=0,pady=5,padx=5)
    code_label.grid(row = 1, column = 0, pady=5)
    start_timer.grid(row=2, column=0, pady=5, padx=5)
    answer_label.grid(row = 3, column=0,pady=5)
    changeId.grid(row=0, column=8, padx=5)
    gameId.grid(row=0, column=7, padx=5)
    
    updatePlayerButtons()

get_players = tk.Button(root, text="Update Players", command=getPlayers,bg="white",fg="black")
get_players.grid(row = 0, column=0,pady=5,padx=5)

input_game_id = tk.StringVar()

gameId = tk.Entry(root, textvariable=input_game_id, width=4)
gameId.grid(row=0, column=7, padx=5)



changeId = tk.Button(root, text="Change game", command=changeGame, bg="white", fg="black")
changeId.grid(row=0, column=8, padx=5)



def displayAnswer(answer=""):
    answer_label.config(text=answer)



# Create labels, entry widgets, plus buttons, and minus buttons
def updatePlayerButtons():
    global label_var
    label_var = [tk.StringVar() for _ in players]
    entry_var = [tk.StringVar() for _ in players]
    
    for i, player in enumerate(players):
        label = tk.Label(root, textvariable=label_var[i])
        label_var[i].set(f"{player}: {scores[player]}")
        label.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # Create entry widget
        entry = tk.Entry(root, textvariable=entry_var[i], width=5)
        entry.grid(row=i, column=4, padx=5)

        # Create plus button
        plus_button = tk.Button(root, text="+", command=lambda i=i: update_score(i, int(entry_var[i].get())), bg="green", fg="white")
        plus_button.grid(row=i, column=5, padx=5)

        # Create minus button
        minus_button = tk.Button(root, text="-", command=lambda i=i: update_score(i, -int(entry_var[i].get())), bg="red", fg="white")
        minus_button.grid(row=i, column=6, padx=5)

        # Create increase button
        increase_button = tk.Button(root, text="Right", command=lambda i=i: update_score(i, 0, correct=True, question=True), bg="green", fg="white")
        increase_button.grid(row=i, column=2, padx=5)

        # Create decrease button
        decrease_button = tk.Button(root, text="Wrong", command=lambda i=i: update_score(i, 0, question=True), bg="red", fg="white")
        decrease_button.grid(row=i, column=3, padx=5)
    
updatePlayerButtons()



# os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
# os.environ['SDL_VIDEODRIVER'] = 'windib'




rounds = getGame(1)


#customcat = ["CAR MAKERS", [["Prius","Toyota",False],["Ranger","Ford",False],["Enzo","Ferrari",False],["Scirocco","Volkswagen",False],["Aztek","Pontiac",True]]]



#rounds[0][3] = customcat

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeopardy")
# colors
black = (0,0,0)
white = (255,255,255)
gold = (214,159,76)
red = (255,0,0)
#
currentRound = 1
roundMask = [[True for x in range(5)] for y in range(6)]




def display_text(text, color, size, position):
    font = pygame.font.Font("KORIN.ttf", size)  # None uses the default font
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position,)
    screen.blit(text_surface, text_rect)



def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    current_line_width = 0

    for word in words:
        word_width, _ = font.size(word + " ")
        if word_width > max_width:
            newtext = ""
            for word2 in words:
                if word != word2:
                    newtext+=word2 + " "
                else:
                    half = len(word)//2
                    newtext+=word[:half]+"- " + word[half:] + " "
            return wrap_text(newtext, font, max_width)
        if current_line_width + word_width <= max_width:
            current_line.append(word)
            current_line_width += word_width
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_line_width = word_width

    lines.append(" ".join(current_line))
    return lines


def display_wrapped_text(text, color, size, position, max_width):
    font = pygame.font.Font("KORIN.ttf", size)  # None uses the default font
    wrapped_lines = wrap_text(text, font, max_width*m)

    line_height = font.get_linesize()
    texts_y = []
    y = position[1]
    # if len(wrapped_lines) == 1: texts_y = [y]
    # if len(wrapped_lines) == 2: texts_y = [y-line_height*.5, y+line_height*.5]
    # if len(wrapped_lines) == 3: texts_y = [y-line_height, y, y+line_height]
    # if len(wrapped_lines) == 4: texts_y = [y-line_height*1.5, y-line_height*.5, y+line_height*.5, y+line_height*1.5]
    
    if len(wrapped_lines) % 2 == 0:   #line spacing logic - comment above is the same logic
        for i in range(len(wrapped_lines)):
            midpoint = ((len(wrapped_lines)+1)/2)-1
            if i <= midpoint:
                texts_y.append(y-line_height*(floor(midpoint)-i+.5))
            elif i >= midpoint:
                texts_y.append(y+line_height*(i-ceil(midpoint)+.5))
    else:
        for i in range(len(wrapped_lines)):
            midpoint = ((len(wrapped_lines)+1)/2)-1
            if i == midpoint:
                texts_y.append(y)
            elif i < midpoint:
                texts_y.append(y-line_height*(midpoint-i))
            elif i > midpoint:
                texts_y.append(y+line_height*(i-midpoint))

    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(position[0], texts_y[i]))
        screen.blit(text_surface, text_rect)



timerLength = 8 # length of timer in seconds


# Game loop
while True:
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP: 
            if event.button == 1:
                if display == 1 and currentRound<=2:
                    pos = pygame.mouse.get_pos()
                    if 90*m<pos[1]<height-50:
                        x = pos[0]//(150*m)
                        y = (pos[1]-90*m)//(90*m)
                        if roundMask[x][y]:
                            ques = [x,y]
                            
                            if rounds[currentRound-1][x][1][y][2]: #checks for daily double
                                display = 4
                            else:
                                resetBuzzers()
                                buzzedPlayer = None
                                sleep(.05)
                                display = 2
                                
                            answer = rounds[currentRound-1][ques[0]][1][ques[1]][1]
                            displayAnswer(answer)

                elif display == 2:
                    display += 1
                elif display == 3:
                    roundMask[ques[0]][ques[1]] = False
                    display = 1
                elif display == 4:
                    resetBuzzers()
                    display = 2
                if display == 1 and currentRound == 3:
                    display+=1
                    
                    
                    answer = rounds[currentRound-1][1][1]
                    displayAnswer(answer)
            elif event.button == 3:
                pos = pygame.mouse.get_pos()
                x = pos[0]//(150*m)
                y = (pos[1]-90*m)//(90*m)
                
                if currentRound<=2:
                    if display == 1:
                        roundMask[x][y] = True   
                    elif display == 2:
                        display-=1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if display == 2:
                    startTimer()
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    cluesLeft = 30
    for x in roundMask:
        for y in x:
            if y:
                break
            else:
                cluesLeft-=1
    if cluesLeft == 0:
        currentRound+=1
        roundMask = [[True for x in range(5)] for y in range(6)]
    
    
    screen.fill((7,18,119))  # Fill with blue

    if currentRound<3 and display == 1:
        for i in range(6):
            for j in range(6):
                pygame.draw.rect(screen, black, ((150*i*m,90*j*m),(150*m,90*m)), 2)
        for p in range(6):
            display_wrapped_text(rounds[currentRound-1][p][0],black,20*m,(150*p*m+75*m+1,45*m+1),150)
            display_wrapped_text(rounds[currentRound-1][p][0],white,20*m,(150*p*m+75*m,45*m),150)
        for i in range(6):
            for j in range(1,6):
                if roundMask[i][j-1]:
                    display_text(f"${j*200*currentRound}", black, 30*m, (i*150*m+75*m+2,j*90*m+45*m+2))
                    display_text(f"${j*200*currentRound}", gold, 30*m, (i*150*m+75*m,j*90*m+45*m))
    if currentRound == 3 and display == 1:
        pygame.draw.rect(screen, black, ((width/2-75*m,(height-50)/2-45*m), (150*m,90*m)), 2)
        display_wrapped_text(rounds[currentRound-1][0],black,20*m,((m*900)//2+3,(m*540)//2+3),150)
        display_wrapped_text(rounds[currentRound-1][0],white,20*m,((m*900)//2,(m*540)//2),150)
    if display == 2:
        if currentRound<3:
            question = rounds[currentRound-1][ques[0]][1][ques[1]][0]
            #buzzer logic
            if buzzer.checkBuzz() and buzzedPlayer == None and timer>0:
                buzzedPlayer = buzzer.checkBuzz()
                timer = time()

        else:
            question = rounds[currentRound-1][1][0]
        display_wrapped_text(question, black, 40*m, ((m*900)//2+3,(m*540)//2+3), 540)
        display_wrapped_text(question, white, 40*m, ((m*900)//2,(m*540)//2), 540)
        
    
    if display == 3:
        if currentRound<3:
            answer = rounds[currentRound-1][ques[0]][1][ques[1]][1]
        else:
            answer = rounds[currentRound-1][1][1]
        display_wrapped_text(answer, black, 40*m, ((m*900)//2+3,(m*540)//2+3), 540)
        display_wrapped_text(answer, white, 40*m, ((m*900)//2,(m*540)//2), 540)
    if display == 4:
        display_text("DAILY DOUBLE!", black, 50*m, ((m*900)//2+3,(m*540)//2+3))
        display_text("DAILY DOUBLE!", white, 50*m, ((m*900)//2,(m*540)//2))
    for i,player in enumerate(players):
        color = white
        if player == buzzer.checkBuzz() and display == 2 and timer>0:
            color = red
        display_text(f"{player}: {scores[player]}", color, 20*m, (100+i*150*m,height-25))
        
    if timer>0 and display == 2:
        pygame.draw.rect(screen, black, ((width//2-150*m,height-60),(300*m,4)),1)
        
        lineOffset = round(1000*(time()-timer)*(-300/(timerLength*1000))+150)
        if lineOffset > -150*m:
            pygame.draw.line(screen,red,(width//2-149*m,height-59),(width//2+lineOffset*m,height-59),2)
    

    pygame.display.flip()

    pygame.time.Clock().tick(60)

    root.update()
    
    
# sound when timer over
# daily double
# manual reset
# only buzz in after done reading
