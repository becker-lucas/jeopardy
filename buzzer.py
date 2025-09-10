from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time

def startSession():
    global driver
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('--ignore-certificate-errors')
    op.add_argument('--mute-audio')
    driver = webdriver.Chrome(options=op)
    driver.get("https://buzzin.live/host")

    # create_game = driver.find_element(By.XPATH, '//*[@id="lobbyChooserModal"]/div[1]/div[1]/div/button')
    # create_game.click()
    time.sleep(2)
    game_code = driver.find_element(By.ID,"gameId")

    print(game_code.text)

    return game_code.text


def checkBuzz():
        buzzes = driver.execute_script('return currentBuzzes')
        if len(buzzes)>0:
            name = buzzes[0]['username']
            
            return name
        return None

def reset():
    reset_button = driver.find_element(By.ID,"resetAll")
    reset_button.click()

def getPlayerNames():
    names = []
    currentPlayers = driver.execute_script('return currentPlayers')
    for player in currentPlayers:
        names.append(player["name"])
    return names
        
            
# startSession()
# player = None
# while True:
#     player = checkBuzz(player)
    




#/html/body/div/div[5]/div[4]/div/div/div[3]
#/html/body/div/div[5]/div[4]/div/div/div[3]