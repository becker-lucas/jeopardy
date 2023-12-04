import requests
from bs4 import BeautifulSoup

id = 6338
url = f"http://www.j-archive.com/showgame.php?game_id={id}"  # Replace with the actual URL of the page you want to scrape

# Send a GET request to the URL
response = requests.get(url)

round1 = []
round2 = []
final = []
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract information from the parsed HTML
    # Example: Get the title of the page
    title = soup.title.text


    # Example: Get the categories of the Jeopardy! game
    categories = soup.select('td.category_name')
    for x,category in enumerate(categories):
        if x<6:
            round1.append([category.text,[[] for i in range(5)]])
        elif x<12:
            round2.append([category.text,[[] for i in range(5)]])
        else:
            final = [category.text,[]]
        
    
    
        
    # Example: Get the clues and answers
    clues = soup.select('td.clue')
    for x,clue in enumerate(clues):
        clue_text = clue.find('td', class_='clue_text')
        answer_text = clue.find('em', class_='correct_response')
        if clue_text and answer_text:
            if x<30:
                round1[x%6][1][x//6] = [clue_text.text.strip(), answer_text.text.strip(), False]
            elif 30<=x<60:
                round2[x%6][1][(x-30)//6] = [clue_text.text.strip(), answer_text.text.strip(), False]
            else:
                final[1] = [clue_text.text.strip(),answer_text.text.strip()]

    text = response.text.split('\n')
    for i,line in enumerate(text):
        if "clue_value_daily_double" in line:
            newline = text[i-1].replace(" ","")
            if "DJ" in newline:
                cat = int(newline[newline.find('c')+8])-1
                clue = int(newline[newline.find('clue')+10])-1
                round2[cat][1][clue][2] = True
            else:
                cat = int(newline[newline.find('c')+7])-1
                clue = int(newline[newline.find('clue')+9])-1
                round1[cat][1][clue][2] = True
    
    
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

