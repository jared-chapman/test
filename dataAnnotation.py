import requests
from bs4 import BeautifulSoup

TEST_URL = "https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub?pli=1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def getCoordinatesFromURL(url, debug = False):
    coordinates = []
    max_x = 0
    max_y = 0

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    for row in rows[1:]: # skip header row
        data = row.find_all("span")
        x = int(data[0].get_text(strip=True))
        c = data[1].get_text(strip=True)
        y = int(data[2].get_text(strip=True))
        coordinates.append([x, y, c])
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    if debug: print (coordinates)
    return {"coordinates": coordinates, "max_x": max_x, "max_y": max_y}


# This could surely be optimized with a hash function or something
# but unless we're expecting very large data sets, this is how
# I would write it for readability
def printCoordinates(coordinates, max_x, max_y):
    # initialize empty grid
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # populate grid with existing coordinate values
    for c in coordinates:
        x = c[0]
        y = max_y - c[1] # otherwise would be flipped
        character = c[2]
        grid[y][x] = character
    
    for row in grid:
        print("".join(row))


def main(url):
    coordinates = getCoordinatesFromURL(url)
    printCoordinates(**coordinates)

# main(TEST_URL)
main("https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub")