import requests
from bs4 import BeautifulSoup

def get_daily_double_clues(game_id):
    url = f"https://j-archive.com/showgame.php?game_id={game_id}"
    response = requests.get(url)
    DDs = []
    if response.status_code == 200:
        text = response.text.split('\n')
        for i,line in enumerate(text):
            if "clue_value_daily_double" in line:
                newline = text[i-1].replace(" ","")
                if "DJ" in newline:
                    print(f"{newline[newline.find('c')+8]},{newline[newline.find('clue')+10]}")
                else:
                    print(f"{newline[newline.find('clue')+7]},{newline[newline.find('clue')+9]}")
                #print(newline[newline.find('c')+8])
                
                #print(newline)
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

if __name__ == "__main__":
    game_id = 6338  # Change this to the desired game ID
    get_daily_double_clues(game_id)


