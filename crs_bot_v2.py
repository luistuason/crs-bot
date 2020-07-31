import requests
from bs4 import BeautifulSoup

def get_courses(soup):
    table = soup.find('table')
    table_rows = table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)

    courses = [res[x][1] for x in range(len(res))]
    for x in range(len(courses)):
        a = courses[x]
        b = a.split()[:2]
        courses[x] = " ".join(b)

    return set(courses)

def main():
    URL = 'https://crs.upd.edu.ph/schedule/120192/eee'

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    courses = get_courses(soup)

    find = ["EEE 141", "EEE 143", "EEE 145", "EEE 147", "EEE 148"]
    for y in find:
        if y in courses:
            print("\nBROOO MERON NANG "+y+"\n")
        else:
            print("Wala pang "+y)


if __name__ == "__main__":
    print()
    main()
    print()