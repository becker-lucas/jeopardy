import pygame
import sys
from scrape import round1, round2, final
from math import floor, ceil
import tkinter as tk
import os
from tkinter import *

print(final)

root = tk.Tk()
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
#embed.grid(columnspan = (600), rowspan = 500) # Adds grid
#embed.pack(side = LEFT) #packs window to the left

players = ["becker","ian","blake"]
scores = {player:0 for player in players}

display = 1 # 1-board 2-question 3-answer 4-final

def update_score(player, amount, correct = False, question = False):
    global display
    scores[players[player]] += amount

    if question and display == 2:
        if correct:
            money = (ques[1]+1)*200*currentRound
            display += 1
        else:
            money = -(ques[1]+1)*200*currentRound
        scores[players[player]] += money
    elif question and display == 3:
        display = 1
        displayAnswer()
    label_var[player].set(f"{players[player]}: {scores[players[player]]}")


label_var = [tk.StringVar() for _ in players]
entry_var = [tk.StringVar() for _ in players]

answer_label = tk.Label(root, text="")
answer_label.grid(row = len(players), column=0,pady=5)

def displayAnswer(answer=""):
    answer_label.config(text=answer)

# Create labels, entry widgets, plus buttons, and minus buttons
for i, player in enumerate(players):
    label = tk.Label(root, textvariable=label_var[i])
    label_var[i].set(f"{player}: {scores[player]}")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

    # Create entry widget
    entry = tk.Entry(root, textvariable=entry_var[i], width=5)
    entry.grid(row=i, column=3, padx=5)

    # Create plus button
    plus_button = tk.Button(root, text="+", command=lambda i=i: update_score(i, int(entry_var[i].get())), bg="green", fg="white")
    plus_button.grid(row=i, column=4, padx=5)

    # Create minus button
    minus_button = tk.Button(root, text="-", command=lambda i=i: update_score(i, -int(entry_var[i].get())), bg="red", fg="white")
    minus_button.grid(row=i, column=5, padx=5)

    # Create increase button
    increase_button = tk.Button(root, text="Right", command=lambda i=i: update_score(i, 0, correct=True, question=True), bg="green", fg="white")
    increase_button.grid(row=i, column=1, padx=5)

    # Create decrease button
    decrease_button = tk.Button(root, text="Wrong", command=lambda i=i: update_score(i, 0, question=True), bg="red", fg="white")
    decrease_button.grid(row=i, column=2, padx=5)




os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'



pygame.init()
rounds = [round1,round2,final]

m = 1 #size modifier
width, height = 900*m, 540*m+50

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeopardy")
black = (0,0,0)
white = (255,255,255)
gold = (214, 159, 76)
currentRound = 2
roundMask = [[False for x in range(5)] for y in range(6)]
roundMask[0][0] = True



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
    wrapped_lines = wrap_text(text, font, max_width)

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



# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP: 
            if display == 1:
                pos = pygame.mouse.get_pos()
                if 90*m<pos[1]<height-50:
                    x = pos[0]//(150*m)
                    y = (pos[1]-90*m)//(90*m)
                    if roundMask[x][y]:
                        ques = [x,y]
                        roundMask[x][y] = False
                        display = 2
                        answer = rounds[currentRound-1][ques[0]][1][ques[1]][1]
                        displayAnswer(answer)

            elif display == 2:
                display += 1
            elif display == 3:
                display = 1
                displayAnswer()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
        display_wrapped_text(rounds[currentRound-1][0],black,20*m,(150*p*m+75*m+1,45*m+1),150)
        display_wrapped_text(rounds[currentRound-1][0],white,20*m,(150*p*m+75*m,45*m),150)
    if display == 2:
        question = rounds[currentRound-1][ques[0]][1][ques[1]][0]
        display_wrapped_text(question, black, 40*m, ((m*900)//2+3,(m*540)//2+3), 540)
        display_wrapped_text(question, white, 40*m, ((m*900)//2,(m*540)//2), 540)
    
    if display == 3:
        answer = rounds[currentRound-1][ques[0]][1][ques[1]][1]
        display_wrapped_text(answer, black, 40*m, ((m*900)//2+3,(m*540)//2+3), 540)
        display_wrapped_text(answer, white, 40*m, ((m*900)//2,(m*540)//2), 540)
    for i,player in enumerate(players):
        display_text(f"{player}: {scores[player]}", white, 20*m, (100+i*200*m,height-25))

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

    pygame.display.flip()

    pygame.time.Clock().tick(60)

    root.update()